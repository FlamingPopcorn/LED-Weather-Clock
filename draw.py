from bmp_to_array import bmp_to_array

# Draw Numbers in a 3 x 5 rectangle
#   0  1  2
#   3  4  5
#   6  7  8
#   9  10 11
#   12 13 14
def draw_number(coordX, coordY, num, matrix):
    from main import time_color, off
    if (num == '0'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,8,9,11,12,13,14]:
                matrix.set_pixel((coordX + pixel % 3),(coordY + pixel // 3), time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '1'):
        for pixel in range(0,15):
            if pixel in [2,5,8,11,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '2'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,6,7,8,9,12,13,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '3'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,6,7,8,11,12,13,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '4'):
        for pixel in range(0,15):
            if pixel in [0,2,3,5,6,7,8,11,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '5'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,6,7,8,11,12,13,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '6'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,6,7,8,9,11,12,13,14]:
                matrix.set_pixel((coordX + pixel % 3),(coordY + pixel // 3), time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '7'):
        for pixel in range(0,15):
            if pixel in [0,1,2,5,8,11,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '8'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,7,8,9,11,12,13,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

    elif (num == '9'):
        for pixel in range(0,15):
            if pixel in [0,1,2,3,5,6,7,8,11,12,13,14]:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 3,coordY + pixel // 3, off)

# Draw Letters in a 5 x 5 rectangle
#   0  1  2  3  4
#   5  6  7  8  9
#   10 11 12 13 14
#   15 16 17 18 19
#   20 21 22 23 24
def draw_letter(coordX: int, coordY: int, letter: str, matrix):
    from main import time_color, off
    if (letter == 'M'):
        for pixel in range(0,25):
            if pixel in [0,4,5,6,8,9,10,12,14,15,19,20,24]:
                matrix.set_pixel((coordX + pixel % 5),(coordY + pixel // 5), time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'T'):
        for pixel in range(0,25):
            if pixel in [0,1,2,3,4,7,12,17,22]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'W'):
        for pixel in range(0,25):
            if pixel in [0,4,5,9,10,12,14,15,16,18,19,20,24]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'R'):
        for pixel in range(0,25):
            if pixel in [0,1,2,3,5,9,10,11,12,13,15,18,20,24]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'F'):
        for pixel in range(0,25):
            if pixel in [0,1,2,3,4,5,10,11,12,15,20]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'S'):
        for pixel in range(0,25):
            if pixel in [0,1,2,3,4,5,10,11,12,13,14,19,20,21,22,23,24]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)

    elif (letter == 'U'):
        for pixel in range(0,15):
            if pixel in [0,4,5,9,10,14,15,19,21,22,23]:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, time_color)
            else:
                matrix.set_pixel(coordX + pixel % 5,coordY + pixel // 5, off)


# Draw the time from a corner and datetime object
def draw_time(coordX, coordY, t, matrix):
    from main import time_color, get_digits_string
    # 12 Hour Time
    if t[3] > 12:
        hours = get_digits_string(t[3] % 12)
    elif  t[3] == 0:
        hours = get_digits_string(12)
    else:
        hours = get_digits_string(t[3])
    minutes = get_digits_string(t[4])
    
    draw_number(coordX, coordY, hours[0], matrix)
    draw_number(coordX + 4, coordY, hours[1], matrix)

    # Draw Colon Time Seperator
    matrix.set_pixel(coordX + 8, coordY + 1, time_color)
    matrix.set_pixel(coordX + 8, coordY + 3, time_color)

    draw_number(coordX + 10, coordY, minutes[0], matrix)
    draw_number(coordX + 14, coordY, minutes[1], matrix)

    matrix.show()

def draw_weekday(coordX: int, coordY: int, weekday: int, matrix):
    weekdays = ["M", "T", "W", "R", "F", "S", "U"]
    draw_letter(coordX, coordY, weekdays[weekday], matrix)

# Draw weather icons at specified XY coord
def draw_weather(coordX, coordY, weather, matrix):
    print(f"The current weather is: {weather}")

    # Specific conditions
    if weather["description"] == "few clouds":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("./weather_icons/few_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])
        else:
            # print("drawing night few clouds")
            pixel_array = bmp_to_array("./weather_icons/few_clouds_night.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["description"] == "broken clouds":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("./weather_icons/broken_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])
        else:
            # print("drawing night few clouds")
            pixel_array = bmp_to_array("./weather_icons/broken_clouds.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    # Main Generic conditions
    elif weather["main"] == "Clouds":
        pixel_array = bmp_to_array("./weather_icons/cloudy.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["main"] == "Clear":
        if (weather["icon"][2] == 'd'):
            pixel_array = bmp_to_array("./weather_icons/clear.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])
        else:
            pixel_array = bmp_to_array("./weather_icons/clear_night.bmp")
            for pixel in range(len(pixel_array[0])):
                matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["main"] == "Rain":
        pixel_array = bmp_to_array("./weather_icons/rainy.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["main"] == "Thunderstorm":
        pixel_array = bmp_to_array("./weather_icons/thunderstorm.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])
    
    elif weather["main"] == "Snow":
        pixel_array = bmp_to_array("./weather_icons/snow.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["main"] == "Mist":
        pixel_array = bmp_to_array("./weather_icons/mist.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    elif weather["main"] == "Haze":
        pixel_array = bmp_to_array("./weather_icons/haze.bmp")
        for pixel in range(len(pixel_array[0])):
            matrix.set_pixel(coordX + pixel % pixel_array[2], coordY + pixel // pixel_array[1], pixel_array[0][pixel])

    else:
        print(f"condition not declared: {weather}")
    matrix.show()

def draw_temp(coordX, coordY, temp, matrix):
    print(f"The current tempurature is: {temp}F")

    draw_number(coordX, coordY, str(round(temp))[0], matrix)
    draw_number(coordX + 4, coordY, str(round(temp))[1], matrix)
    matrix.set_pixel(coordX + 7, coordY, (255,0,0))