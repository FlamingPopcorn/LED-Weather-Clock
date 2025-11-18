from matrix import Matrix
#from neopixel import Neopixel
from time import localtime, sleep, gmtime, mktime
from machine import Pin, RTC, Timer
from requests import get

import network
import socket
import struct

from bmp_to_array import bmp_to_array
import draw

############################################################################
#                              START CONFIG                                #
############################################################################

# Number of LED Pixels
Width_pixels = 32
Height_pixels = 16
height_per_panel = 8
number_pixels = Width_pixels * Height_pixels

# DIO Pin for LED Matrix
LED_PIN = 28

# Day and Night times in 24 hour time
start_day_time = 8
start_night_time = 21

# LED Strip Brightness
brightness_day = 25
brightness_night = 2

red = (255, 0 ,0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
purple = (130, 0 , 255)
off = (0, 0, 0)

time_color = purple
border_color = (160, 0, 255)

# RTC object in the form of (year, month, day, weekday, hours, minutes, seconds, subseconds)
# Note for weekday: Monday = 0 .. Sunday == 6
startDay = 4
startMonth = 11
startYear = 2025
weekday = 1

# Wifi settings for ntp
ssid = ""
password = ""
maxRetryCount = 10

# ntp settings
timezone_offset = -5
host = "pool.ntp.org"

# Weather settings - API Docs: https://openweathermap.org/api
weather_api_key = ""
# zip_code = 
# country_code = ""
# get_location_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={weather_api_key}"

lat = 
lon = 

get_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={weather_api_key}"

# Update Intervals in minutes
brightness_update_interval = 5
weather_update_interval = 10
weekday_update_interval = 60

# Update Intervals in hours
RTC_resync_interval = 24

############################################################################
#                               END CONFIG                                 #
############################################################################

# Translate 1D linear coords to the snake wiring coords
def unsnake(pos):
    if (pos % 2 == 1):
        return pos - 1 + Height_pixels - pos % Height_pixels * 2 
    else:
        return pos

# Draw a border around the matrix
def draw_border():
    for pixel in range(0, Height_pixels):
        matrix.set_pixel(0, pixel, border_color)
        matrix.set_pixel(Width_pixels - 1, pixel, border_color) 

    for pixel in range(1, Width_pixels - 1):
        matrix.set_pixel(pixel, 0, border_color)
        matrix.set_pixel(pixel, Height_pixels - 1, border_color)
    matrix.show()

# Convert int to array of individual digits
def get_digits_string(number):
    num_str = str(number)
    if (len(str(num_str)) < 2):
        num_str = "0" + num_str
    return [str(digit) for digit in num_str]

# Draw everything else

# Sets brightness to set night time brightness
def nightTime():
    matrix.brightness(brightness_night)
    matrix.show()

# Sets brightness to set day time brightness
def dayTime():
    matrix.brightness(brightness_day)
    matrix.show()

# Connect to WLAN
def connect():
    led.on()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    attempt = 0
    while (wlan.isconnected() is False and attempt < maxRetryCount):
        print(f"Atempting to connect to configure network... try: {attempt + 1}")
        led.on()
        sleep(1)
        led.off()
        sleep(1)
        attempt += 1
    led.off()
    return wlan

# Sync time via configured ntp server over internet
def sync_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

# Get weather from Open Weather API
def get_weather():
    weather = get(get_weather_url)
    return weather

# Draw Weather and temp

# RTC sync interupt handler
def resync_RTC(_):
    global wlan
    global ssid
    if (wlan.isconnected() is False and ssid != ""):
        wlan = connect()
    sync_time()

# Weather update interupt handler
def update_weather(_):
    current_weather = get_weather()
    draw.draw_weather(25, 1, current_weather.json()["weather"][0], matrix)
    draw.draw_temp(23,9, current_weather.json()["main"]["temp"], matrix)

# Brightness update interupt handler
def update_brightness(_):
    t = localtime()
    if (t[3] >= start_night_time  or t[3] <= start_day_time):
        nightTime()
    else:
        dayTime()
    draw_border()

# Weekday update interupt handle
def update_weekday(_):
    t = localtime()
    draw.draw_weekday(20, 2, t[6], matrix)

############################################################################
#                        Main Setup Code and Loop                          #
############################################################################

# Sets NTP offset based of configured timezone
NTP_DELTA = 2208988800 - 3600 * timezone_offset

# setup Pico W LED Pin
led = Pin("LED", Pin.OUT)

# Declare LED Matrix Object
matrix = Matrix(Height_pixels, Width_pixels, height_per_panel, LED_PIN)

# Blank matrix at the beginning
matrix.fill(off)
matrix.show()

# Connects to wifi is ssid is set or else uses hardcoded time
if (ssid != ""):
    # Setup RTC time to current ntp time
    wlan = connect()
    sync_time()
    RTC().datetime()
    print(f"Time set via ntp! {wlan.ifconfig()}")
else:
    # Setup RTC time to current configured time
    timeStart = (startYear, startMonth, startDay, weekday, 0, 0, 0, 0)
    RTC().datetime(timeStart)
    print("Time set via hardcoded time!")


# Software timers to run update functions periodically
soft_timer1 = Timer(mode=Timer.PERIODIC, period=1000 * 60 * brightness_update_interval, callback=update_brightness)
soft_timer2 = Timer(mode=Timer.PERIODIC, period=1000 * 60 * weather_update_interval, callback=update_weather)
soft_timer3 = Timer(mode=Timer.PERIODIC, period=1000 * 60 * 60 * RTC_resync_interval, callback=resync_RTC)
soft_timer4 = Timer(mode=Timer.PERIODIC, period=1000 * 60 * weekday_update_interval, callback=update_weekday)

# Run initial update after timers are setup
update_brightness(None)
update_weather(None)
update_weekday(None)

## Main Loop ##    
while(True):
    #time object is in form (year, month, mday, hour, minute, second, weekday, yearday)
    t = localtime()

    # Draw clock time
    draw.draw_time(2,2,t, matrix)
    
    # Debug print the current RTC time to serial console
    print(f"Current RTC time is: {t}")
    sleep(1)