# LED-Weather-Clock
A clock designed to use a WS2812B LED matrix and a Pi Pico. This program uses the OpenWeather API and ntp to set the RTC and display the time and local weather. You can edit the weather icons to your liking (Note: BMP files' bytes are written upside down, and I haven't accounted for this yet).

# Wiring
- A 5V power supply should be wired to the VBUS and GND pins and the 5V and GND pins on the LED strip
- Wire the LED strip's DIO in pin to GPIO 28 on the pico

# Flashing the Pi Pico
1. Install micropython onto your pico with the latest official release
2. Upload the project files to your pico with an IDE like Thonny or VSCode with the MicroPico Extension
3. Unplug the pico and power it again. It should be running the program
