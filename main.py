import pygame as pg
import sys
from os import path


from settings import *
from sprites import *
from generators import *
from camera import *


class Game:

    def __init__(self):
        """Initialize screen, pygame, map data, and settings."""
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.map = Generate()

    def new(self):
        """Initialize all variables and do all the setup for a new game."""
        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.map_data = self.map.generate_map_data()
        self._set_grid(self.map_data)
        self.player = Player(self, 10, 10)
        self.camera = Camera(self.map.width, self.map.height)

    def _set_grid(self, map_data):
        for row_nb, row in enumerate(map_data):
            for col_nb, tile in enumerate(row):
                if tile == 0:
                    tile_data = 'pixel dirt square'
                if tile == 1:
                    tile_data = 'pixel square grass'
                if tile == 2:
                    tile_data = 'pixel square flower'
                if tile == 3:
                    tile_data = 'pixel square tree'
                Tile(self, tile_data, row_nb, col_nb)

    def run(self):
        """Game loop."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # Catch all events.
            self.events()
            # Update data.
            self.update()
            # Draw updated screen.
            self.draw()

    def quit(self):
        """Quit the game."""
        pg.quit()
        sys.exit()

    def update(self):
        # Update everything here.
        self.all_sprites.update()
        self.camera.update(self.player)

    def _update_background(self, x, y):
        """Will update the tile data for the background."""
        self.map_data[x][y] = 0
        self._set_grid(self.map_data)

    def draw(self):
        """Draw the screen."""
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        """Catch all events here."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pg.K_RETURN:
                    x, y = self.player.current_position()
                    self._update_background(x, y)


# Create game object.
g = Game()
while True:
    g.new()
    # Main Game Loop
    g.run()
