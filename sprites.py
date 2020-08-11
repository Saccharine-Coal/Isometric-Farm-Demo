import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    """Class that holds everything for the Player Character."""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/player tile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        """Moves the position of the player in cartesian coordinates."""
        self.x += dx
        self.y += dy

    def update(self):
        """Updates the isometric position of the player."""
        self.rect.x, self.rect.y = self._convert()

    def _convert(self):
        """Converts cartesian coordinates to isometric."""
        x = self.x
        y = self.y
        cart_x = x * TILEWIDTH_HALF
        cart_y = y * TILEHEIGHT_HALF
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        return iso_x, iso_y

    def current_position(self):
        """Current position of the player in isometric coordinates."""
        return self.x, self.y


class Tile(pg.sprite.Sprite):
    """All entities that make up the grid background is currently handled in this class."""
    def __init__(self, game, tile_data, x, y):
        self.groups = game.all_sprites, game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(f"""images/{tile_data}.png""").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # Convert cartesian to isometric coordinates
        cart_x = x * TILEWIDTH_HALF
        cart_y = y * TILEHEIGHT_HALF
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        self.rect.x = iso_x
        self.rect.y = iso_y
