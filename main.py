from neopixel import Neopixel
from time import localtime, sleep, gmtime, mktime
from machine import Pin, RTC, Timer
from requests import get

import network
import socket
import struct

from bmp_to_array import bmp_to_array

############################################################################
#                              START CONFIG                                #
############################################################################

# Number of LED Pixels
Length_pixels = 32
Height_pixels = 8
number_pixels = Length_pixels * Height_pixels

# DIO Pin for LED Strip
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
startDay = 10
startMonth = 11
startYear = 2025
weekday = 0

# Wifi settings for ntp
ssid = ""
password = ""
maxRetryCount = 10

# ntp settings
timezone_offset = 
host = "pool.ntp.org"

# Weather settings - API Docs: https://openweathermap.org/api
weather_api_key = ""
# zip_code = 
# country_code = ""
# get_location_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={weather_api_key}"

lat = 
lon = 

get_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"

# Update Intervals in minutes
brightness_update_interval = 5
weather_update_interval = 10

# Update Intervals in hours
RTC_resync_interval = 24

############################################################################
#                               END CONFIG                                 #
############################################################################

# Translate regular 2D XY coords to the snake wiring coords
def XY_to_snake(coordX, coordY):
    if coordX % 2 == 0: # Even index rows are same as linear indexing
        snakePos = coordX * Height_pixels + coordY
    else: # Odd index rows are reversed due to Snake indexing
        snakePos = coordX * Height_pixels + (Height_pixels - 1 - coordY)
    # print(f"Debug: Snake Pos is = {snakePos}")
    return snakePos

# Translate 1D linear coords to the snake wiring coords
def unsnake(pos):
    if (pos % 2 == 1):
        return pos - 1 + Height_pixels - pos % Height_pixels * 2 
    else:
        return pos

# Draw a border around the matrix
def draw_border():
    strip.set_pixel_line(0, Height_pixels - 1, border_color)
    strip.set_pixel_line(number_pixels - 1 - Height_pixels, number_pixels - 1, border_color)

    for pixel in range(1,Length_pixels - 1):
        strip.set_pixel(XY_to_snake(pixel, 0), border_color)
        strip.set_pixel(XY_to_snake(pixel, Height_pixels - 1), border_color)
    strip.show()

# Convert int to array of individual digits
def get_digits_string(number):
    num_str = str(number)
    if (len(str(num_str)) < 2):
        num_str = "0" + num_str
    return [str(digit) for digit in num_str]

# Draw Numbers in a 3 x 5 rectangle
#   0  1  2
#   3  4  5
#   6  7  8
#   9  10 11
#   12 13 14
def draw_number(coordX, coordY, num, strip):
    if (num == '0'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,8,9,11,12,13,14]:
                strip.set_pixel(XY_to_snake((coordX + pixel % 3),(coordY + pixel // 3)), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '1'):
        for pixel in range(0,15):
            if pixel in [2,5,8,11,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '2'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,6,7,8,9,12,13,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '3'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,6,7,8,11,12,13,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '4'):
        for pixel in range(0,15):
            if pixel in [0,2,3,5,6,7,8,11,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '5'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,6,7,8,11,12,13,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '6'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,6,7,8,9,11,12,13,14]:
                strip.set_pixel(XY_to_snake((coordX + pixel % 3),(coordY + pixel // 3)), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '7'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,8,11,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '8'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,7,8,9,11,12,13,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

    elif (num == '9'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,7,8,11,12,13,14]:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), time_color)
            else:
                strip.set_pixel(XY_to_snake(coordX + pixel % 3,coordY + pixel // 3), off)

# Draw the time from a corner and datetime object
def draw_time(coordX, coordY, t, strip):
    # 12 Hour Time
    if t[3] > 12:
        hours = get_digits_string(t[3] % 12)
    elif  t[3] == 0:
        hours = get_digits_string(12)
    else:
        hours = get_digits_string(t[3])
    minutes = get_digits_string(t[4])
    
    draw_number(coordX, coordY, hours[0], strip)
    draw_number(coordX + 4, coordY, hours[1], strip)

    # Draw Colon Time Seperator
    strip.set_pixel(XY_to_snake(coordX + 8, coordY + 1), time_color)
    strip.set_pixel(XY_to_snake(coordX + 8, coordY + 3), time_color)

    draw_number(coordX + 10, coordY, minutes[0], strip)
    draw_number(coordX + 14, coordY, minutes[1], strip)

    strip.show()

# Sets brightness to set night time brightness
def nightTime():
    strip.brightness(brightness_night)
    strip.show()

# Sets brightness to set day time brightness
def dayTime():
    strip.brightness(brightness_day)
    strip.show()

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

# Draw weather icons at specified XY coord
def draw_weather(coordX, coordY, weather):
    print(f"The current weather is: {weather}")

    # Specific conditions
    if weather["description"] == "few clouds":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("few_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])
        else:
            # print("drawing night few clouds")
            pixel_array = bmp_to_array("few_clouds_night.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["description"] == "broken clouds":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("broken_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])
        else:
            # print("drawing night few clouds")
            pixel_array = bmp_to_array("broken_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    # Main Generic conditions
    elif weather["main"] == "Clouds":
        pixel_array = bmp_to_array("cloudy.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["main"] == "Clear":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("clear.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])
        else:
            pixel_array = bmp_to_array("clear_night.bmp")
            for pixel in range(len(pixel_array[0])):
                strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["main"] == "Rain":
        pixel_array = bmp_to_array("rainy.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["main"] == "Thunderstorm":
        pixel_array = bmp_to_array("thunderstorm.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])
    
    elif weather["main"] == "Snow":
        pixel_array = bmp_to_array("snow.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["main"] == "Mist":
        pixel_array = bmp_to_array("mist.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    elif weather["main"] == "Haze":
        pixel_array = bmp_to_array("haze.bmp")
        for pixel in range(len(pixel_array[0])):
            strip.set_pixel(XY_to_snake(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1]), pixel_array[0][pixel])

    else:
        print(f"condition not declared: {weather}")
    strip.show()

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
    draw_weather(25, 1, current_weather.json()["weather"][0])

# Brightness update interupt handler
def update_brightness(_):
    t = localtime()
    if (t[3] >= start_night_time  or t[3] <= start_day_time):
        nightTime()
    else:
        dayTime()
    draw_border()

############################################################################
#                        Main Setup Code and Loop                          #
############################################################################

# Sets NTP offset based of configured timezone
NTP_DELTA = 2208988800 - 3600 * timezone_offset

# setup Pico W LED Pin
led = Pin("LED", Pin.OUT)

# Declare LED Strip Object
strip = Neopixel(number_pixels, 0, LED_PIN, "GRB")

# Blank strip at the beginning
strip.set_pixel_line(0,number_pixels - 1, off)
strip.show()

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

# Run initial update after timers are setup
update_brightness(None)
update_weather(None)

## Main Loop ##    
while(True):
    #time object is in form (year, month, mday, hour, minute, second, weekday, yearday)
    t = localtime()

    # Draw clock time
    draw_time(1,1,t,strip)
    
    # Debug print the current RTC time to serial console
    print(f"Current RTC time is: {t}")

    sleep(1)
