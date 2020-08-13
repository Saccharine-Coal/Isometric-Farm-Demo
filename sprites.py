import pygame as pg

from settings import *
from converter import *
import random

class Player(pg.sprite.Sprite):
    """Class that holds everything for the Player Character."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/overlay player trans.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.iso = Converter()

    def move(self, dx=0, dy=0):
        """Moves the position of the player in cartesian coordinates."""
        self.x += dx
        self.y += dy

    def update(self):
        """Updates the isometric position of the player."""
        #print(f'''player cart pos: {self.x}, {self.y}''')
        self.rect.x, self.rect.y = self.iso.convert_cart(self.x, self.y)

    def current_position(self):
        """Current position of the player in isometric coordinates."""
        return self.x, self.y


class Tile(pg.sprite.Sprite):
    """All entities that make up the grid background is currently handled in this class."""
    def __init__(self, grid, game, data, x, y):
        self.data = data
        self.flag = False
        self.sprite_init = True
        self.grow = False
        self.game = game
        self.x, self.y = x, y
        if self.data != 0:
            self.init_sprite()
            self.load_sprite()

    def init_sprite(self):
        self.groups = self.game.tiles #, game.all_sprites'''
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sprite_init = False

    def load_sprite(self):
        self.check_data()
        self.image = pg.image.load(f"""images/{self.tile_data}.png""").convert_alpha()
        self.rect = self.image.get_rect()
        self.iso = Converter()
        # Convert cartesian to isometric coordinates
        self.rect.x, self.rect.y = self.iso.convert_cart(self.x, self.y)

    def check_data(self):
        if self.data == 1:
            self.tile_data = 'overlay tree'
        if self.data == 2:
            self.tile_data = 'pixel dirt square'
        if self.data == 3:
            self.tile_data = 'pixel square grass'
        if self.data == 4:
            self.tile_data = 'overlay seed'
        if self.data == 5:
            self.tile_data = 'overlay crop1'
        if self.data == 6:
            self.tile_data = 'overlay crop2'

    def update_tile_image(self):
        if self.sprite_init:
            self.init_sprite()
            self.load_sprite()
            self.flag = False
        else:
            self.check_data()
            self.image = pg.image.load(f"""images/{self.tile_data}.png""").convert_alpha()
            self.flag = False


class Grid:
    def __init__(self, game, data, width, height):
        """Initialize a grid object with dimensions width x height that contains
        Tile objects with specified data."""
        self.width = width * TILEWIDTH
        self.height = height * TILEHEIGHT
        self.grid_data = [[data for x in range(width)] for y in range(height)]
        if data == 10:
            for row_nb, row in enumerate(self.grid_data):
                for col_nb, tile in enumerate(row):
                    self.grid_data[row_nb][col_nb] = Tile(self, game, random.randint(0, 1), row_nb, col_nb)
        else:
            for row_nb, row in enumerate(self.grid_data):
                for col_nb, tile in enumerate(row):
                    self.grid_data[row_nb][col_nb] = Tile(self, game, random.randint(2, 3), row_nb, col_nb)

    def update_tile(self, data, x, y):
        self.grid_data[x][y].flag = True
        self.grid_data[x][y].data = data

    def check_update_grid(self):
        for row_nb, row in enumerate(self.grid_data):
            for col_nb, tile in enumerate(row):
                if tile.flag:
                    tile.update_tile_image()

