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
        print(f'''player cart pos: {self.x}, {self.y}''')
        self.rect.x, self.rect.y = self.iso.convert_cart(self.x, self.y)

    def current_position(self):
        """Current position of the player in isometric coordinates."""
        return self.x, self.y


class Tile(pg.sprite.Sprite):
    """All entities that make up the grid background is currently handled in this class."""
    def __init__(self, game, tile_data, x, y):
        self.groups = game.tiles #, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(f"""images/{tile_data}.png""").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.iso = Converter()
        # Convert cartesian to isometric coordinates
        iso_x, iso_y = self.iso.convert_cart(self.x, self.y)
        self.rect.x = iso_x
        self.rect.y = iso_y

'''class Grid(pg.sprite.Sprite, Game):
    """All entities that make up the grid background is currently handled in this class."""
    def __init__(self, game, map_data):
        self.groups = game.tiles , game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.iso = Converter()
        self.map_data = map_data

        for row_nb, row in enumerate(self.map_data):
            for col_nb, tile in enumerate(row):
                if tile == 0:
                    tile_data = '128x128 green tile'
                if tile == 1:
                    tile_data = 'overlay seed tile' #pixel square grass
                if tile == 2:
                    tile_data = 'overlay flower1 tile' #pixel square flower
                if tile == 3:
                    tile_data = 'overlay flower2 tile' #pixel square tree
                if tile == 4:
                    tile_data = 'dirt tile'
                image = pg.image.load(f"""images/{tile_data}.png""").convert_alpha()
                rect = image.get_rect()
                x = row_nb
                y = col_nb
                # Convert cartesian to isometric coordinates
                iso_x, iso_y = self.iso.convert_cart(x, y)
                rect.x = iso_x
                rect.y = iso_y
                self.screen.blit(image, rect)'''

