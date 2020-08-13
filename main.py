import pygame as pg
import sys
from os import path


from settings import *
from sprites import *
from generators import *
from camera import *
from converter import *
import threading
import time


class Game:

    def __init__(self):
        """Initialize screen, pygame, map data, and settings."""
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.gen = Generate()
        self.iso = Converter()
        self.interval = 5

    def _run_thread(self):
        """Method that runs forever."""
        while True:
            # Do something
            print('Thread Running!')
            self.grow()
            time.sleep(self.interval)


    def new(self):
        """Initialize all variables and do all the setup for a new game."""
        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.grid_background = Grid(self, 2, W, H)
        self.grid_foreground = Grid(self, 10, W, H)
        self.player = Player(self, 2, 2)
        self.camera = Camera(self.grid_background.width, self.grid_background.height)
        thread = threading.Thread(target=self._run_thread, args=())
        thread.start()                                  # Start the execution

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
        self.grid_background.check_update_grid()
        self.grid_foreground.check_update_grid()
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        """Draw the screen."""
        self.screen.fill(BGCOLOR)
        for tile in self.tiles:
            self.screen.blit(tile.image, self.camera.apply(tile))
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
                    self.grid_background.update_tile(2, x, y)
                    self.grid_foreground.update_tile(4, x, y)
                    self.grid_foreground.grid_data[x][y].grow = True

    def grow(self):
        for row_nb, row in enumerate(self.grid_foreground.grid_data):
            for col_nb, tile in enumerate(row):
                if tile.grow:
                    result = self.gen.generate_random_number(0, 1)
                    if result == 0:
                        tile.data += 1
                        self.grid_foreground.update_tile(tile.data, row_nb, col_nb)


# Create game object.
g = Game()
while True:
    g.new()
    # Main Game Loop
    g.run()
