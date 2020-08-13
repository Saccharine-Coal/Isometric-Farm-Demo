import pygame as pg

from settings import *
from converter import *

class Player(pg.sprite.Sprite):
    """Class that holds everything for the Player Character."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/128x128 player tile.png").convert_alpha()
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
        self.game = game
        # Flags to check if other processes are needed.
        self.flag = False
        self.sprite_init = True
        self.grow = False
        self.x, self.y = x, y
        if self.data != 0:
            self.init_sprite()
            self.load_sprite()

    def init_sprite(self):
        """Creates a sprite."""
        self.groups = self.game.tiles #, game.all_sprites'''
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sprite_init = False

    def load_sprite(self):
        """Gives the sprite an image to show."""
        self.check_data()
        self.image = pg.image.load(f"""images/{self.tile_data}.png""").convert_alpha()
        self.rect = self.image.get_rect()
        self.iso = Converter()
        # Convert cartesian to isometric coordinates
        self.rect.x, self.rect.y = self.iso.convert_cart(self.x, self.y)

    def check_data(self):
        """Checks the data in the Tile object and selects the image to display."""
        if self.data == 1:
            self.tile_data = '128x128 green tile'
        if self.data == 2:
            self.tile_data = 'dirt tile'
        if self.data == 3:
            self.tile_data = 'overlay seed tile'
        if self.data == 4:
            self.tile_data = 'overlay flower1 tile'
        if self.data == 5:
            self.tile_data = 'overlay flower2 tile'

    def update_tile_image(self):
        """Updates the tile with a new image and checks to see if the tile needs a sprite now."""
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
        Tile objects with specified data. All the tile objects are held in a list
        array."""
        self.width = width * TILEWIDTH
        self.height = height * TILEHEIGHT
        self.grid_data = [[data for x in range(width)] for y in range(height)]
        for row_nb, row in enumerate(self.grid_data):
            for col_nb, tile in enumerate(row):
                self.grid_data[row_nb][col_nb] = Tile(self, game, data, row_nb, col_nb)

    def update_tile(self, data, x, y):
        """Updates a tile at the specified coordinates."""
        self.grid_data[x][y].flag = True
        self.grid_data[x][y].data = data

    def check_update_grid(self):
        """Check if the grid needs to be updated."""
        for row_nb, row in enumerate(self.grid_data):
            for col_nb, tile in enumerate(row):
                if tile.flag:
                    tile.update_tile_image()

