def bmp_to_array(filename: str, PrintBMPInfo=0):
    bmp = open(filename, "rb")

    bmp.seek(10)
    bmp_start_offset = int.from_bytes(bytearray(bmp.read(4)), 'little')

    bmp.seek(18)
    bmp_width = int.from_bytes(bytearray(bmp.read(4)), 'little')

    bmp.seek(22)
    bmp_height = int.from_bytes(bytearray(bmp.read(4)), 'little')

    if (PrintBMPInfo):
        print(f"BMP Start Offset: {bmp_start_offset}")
        print(f"BMP Width: {bmp_width}")
        print(f"BMP Height: {bmp_height}")

    bmp.seek(bmp_start_offset)

    bmp_array = [(0,0,0)] * bmp_width * bmp_height
    for pixel in range(bmp_width * bmp_height):
        b = int.from_bytes(bmp.read(1))
        g = int.from_bytes(bmp.read(1))
        r = int.from_bytes(bmp.read(1))

        # I think could do -pixel to index backwards. Potentially need to just do rows backwards
        if ((r, g, b) == (255, 255, 255)):
            bmp_array[pixel] = (0,0,0)
        else:
            bmp_array[pixel] = (r,g,b)

        if (pixel % bmp_width == (bmp_width - 1) and bmp_width % 4 != 0):
            bmp.read(4 - bmp_width % 4)
    bmp.close()
    
    return (bmp_array, bmp_height, bmp_width)