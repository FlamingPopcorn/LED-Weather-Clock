from neopixel import Neopixel
from time import sleep

class Matrix:
    def __init__(self, height, width, panel_height, pin):
        self.height = height
        self.width = width
        self.individual_panel_height = panel_height
        self.total = height * width

        self.matrix = Neopixel(height * width, 0, pin, "GRB")

    # Translate regular 2D XY coords to the snake wiring coords
    def XY_to_snake(self, coordX, coordY):
        panelnum = coordY // self.individual_panel_height
        panelX = coordX % self.width
        panelY = coordY % self.individual_panel_height
        panelpix = self.width * self.individual_panel_height

        if panelnum % 2 == 0 and coordX % 2 == 0: # Even index rows are same as linear indexing
            snakePos = panelX * self.individual_panel_height + panelY + panelpix * panelnum
        elif panelnum % 2 == 0 and panelX % 2 == 1: # Odd index rows are reversed due to Snake indexing
            snakePos = panelX * self.individual_panel_height + (self.individual_panel_height - 1 - panelY) + panelpix * panelnum

        elif panelnum % 2 == 1 and coordX % 2 == 0:
            snakePos = panelpix * (panelnum + 1) - panelX * self.individual_panel_height +  (panelY) - self.individual_panel_height
        elif panelnum % 2 == 1 and coordX % 2 == 1:
            snakePos = panelpix * (panelnum  + 1) - panelX * self.individual_panel_height + (self.individual_panel_height - 1 - panelY) - self.individual_panel_height
        #print(f"Debug: Snake Pos is = {snakePos}")
        return snakePos

    # Translate 1D linear coords to the snake wiring coords
    def unsnake(self, pos):
        if (pos % 2 == 1):
            return pos - 1 + self.individual_panel_height - pos % self.individual_panel_height * 2 
        else:
            return pos
        

    def set_pixel(self, coordX, coordY, color: tuple):
        pos = self.XY_to_snake(coordX, coordY)
        self.matrix.set_pixel(pos, color)

    def fill(self, color: tuple):
        self.matrix.fill(color)

    def brightness(self, brightness: int):
        self.matrix.brightness(brightness)

    def show(self):
        self.matrix.show()
