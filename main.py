import pygame as pg
import sys
from os import path


from settings import *
from sprites import *
from generators import *
from camera import *
from converter import *


class Game:

    def __init__(self):
        """Initialize screen, pygame, map data, and settings."""
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.map = Generate()
        self.iso = Converter()

    def new(self):
        """Initialize all variables and do all the setup for a new game."""
        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.map_background_data = self.map.generate_map_data_blank()
        self.player = Player(self, 2, 2)
        self.camera = Camera(self.map.width, self.map.height)

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

    def draw(self):
        """Draw the screen."""
        self.screen.fill(BGCOLOR)
        self._draw_tiles(self.map_background_data)
        for tile in self.tiles:
            self.screen.blit(tile.image, self.camera.apply(tile))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def _draw_tiles(self, map_data):
        """Draws individual tiles, this creates a new object for each tile."""
        for row_nb, row in enumerate(map_data):
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
                Tile(self, tile_data, row_nb, col_nb)

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

# Create game object.
g = Game()
while True:
    g.new()
    # Main Game Loop
    g.run()
