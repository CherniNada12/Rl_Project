import numpy as np

class GridEnvironment:
    def __init__(self, grid_size=8):
        self.GRID_SIZE = grid_size
        self.CELL_TYPES = {'EMPTY':0,'WALL':1,'PIT':2,'TREASURE':3,'START':4}
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.start_position = {'x':0,'y':7}
        self._create_grid()
    
    def _create_grid(self):
        self.grid.fill(self.CELL_TYPES['EMPTY'])
        self.grid[2,2:5] = self.CELL_TYPES['WALL']
        self.grid[5,2:5] = self.CELL_TYPES['WALL']
        self.grid[3:5,6] = self.CELL_TYPES['WALL']
        self.grid[1,5] = self.CELL_TYPES['PIT']
        self.grid[4,1] = self.CELL_TYPES['PIT']
        self.grid[6,5] = self.CELL_TYPES['PIT']
        self.grid[1,7] = self.CELL_TYPES['TREASURE']
        self.grid[7,0] = self.CELL_TYPES['START']

    def get_cell_type(self, x, y):
        if x<0 or x>=self.GRID_SIZE or y<0 or y>=self.GRID_SIZE:
            return None
        return self.grid[y,x]
    
    def is_terminal(self, x, y):
        return self.get_cell_type(x,y) in [self.CELL_TYPES['TREASURE'], self.CELL_TYPES['PIT']]

    def get_reward(self, x, y):
        if x<0 or x>=self.GRID_SIZE or y<0 or y>=self.GRID_SIZE:
            return -10
        rewards = {self.CELL_TYPES['WALL']:-10,
                   self.CELL_TYPES['PIT']:-50,
                   self.CELL_TYPES['TREASURE']:100}
        return rewards.get(self.grid[y,x], -1)
