class Tile:
    def __init__(self, Tile, data, x, y):
        self.data = data
        self.x = x
        self.y = y

    def update(self, data):
        self.data = data


class Parent:
    def __init__(self):
        self.w = 3
        self.h = 4

    def run(self):
        self.gizmo = Grid(self,0, 3, 4)
        self.show_data(self.gizmo)

    def show_data(self, target):
        for row_nb, row in enumerate(target.grid_data):
            for col_nb, tile in enumerate(row):
                print(target.grid_data[row_nb][col_nb].data)
                '''target.update_tile(10, row_nb, col_nb)
                print(target.grid_data[row_nb][col_nb].data)'''
        '''print("H: " + str(len(target.grid_data)))
        print("W: " + str(len(row)))'''


class Grid:
    def __init__(self, game, data, width, height):
        self.grid_data = [[0 for x in range(width)] for y in range(height)]
        for row_nb, row in enumerate(self.grid_data):
            for col_nb, tile in enumerate(row):
                print(tile)
                if tile == 0:
                    print('Passing first')
                elif tile == 1:
                    print('passing second')
                    del self.grid_data[row_nb][col_nb]
                    self.grid_data[row_nb][col_nb] = 100
                else:
                    print("Else pass")
                    self.grid_data[row_nb][col_nb] = Tile(self, 1, row_nb, col_nb)

    def update_tile(self, data, x, y):
        self.grid_data[x][y].update(data)

    def delete_tile(self, x, y):
        self.grid_data[x][y].update("Don't display an image")


x = Parent()
x.run()
