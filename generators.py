import random

from settings import *


class Generate:
    def __init__(self):
        self.tilewidth = W
        self.tileheight = H
        self.width = W * TILEWIDTH
        self.height = H * TILEHEIGHT

    def generate_map_data(self):
        self.map_data = [
            [random.randint(1, 3) for x in range(self.tilewidth)] for y in range(self.tileheight)
            ]
        return self.map_data

    def generate_map_data_blank(self):
        self.map_data = [
            [0 for x in range(self.tilewidth)] for y in range(self.tileheight)
            ]
        return self.map_data

