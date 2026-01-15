import numpy as np

class RLAgent:
    ACTIONS = {'UP':0,'RIGHT':1,'DOWN':2,'LEFT':3}
    ACTION_NAMES = ['↑','→','↓','←']

    def __init__(self, environment, alpha=0.1, gamma=0.95, epsilon=1.0,
                 epsilon_decay=0.995, epsilon_min=0.01):
        self.env = environment
        self.params = {'alpha':alpha,'gamma':gamma,'epsilon':epsilon,
                       'epsilon_decay':epsilon_decay,'epsilon_min':epsilon_min}
        self.q_table = {}
        self.q_table2 = {}
        self._initialize_q_tables()

    def _initialize_q_tables(self):
        for y in range(self.env.GRID_SIZE):
            for x in range(self.env.GRID_SIZE):
                if self.env.grid[y,x] != self.env.CELL_TYPES['WALL']:
                    key = f"{x},{y}"
                    self.q_table[key] = [0.0]*4
                    self.q_table2[key] = [0.0]*4

    def reset_q_tables(self):
        self._initialize_q_tables()
        self.params['epsilon'] = 1.0

    def choose_action(self, x, y, epsilon=None):
        if epsilon is None:
            epsilon = self.params['epsilon']
        key = f"{x},{y}"
        if np.random.random() < epsilon:
            return np.random.randint(4)
        return np.argmax(self.q_table.get(key,[0]*4))

    def get_next_state(self, x, y, action):
        new_x, new_y = x, y
        if action == self.ACTIONS['UP']: new_y = max(0,y-1)
        elif action == self.ACTIONS['RIGHT']: new_x = min(self.env.GRID_SIZE-1,x+1)
        elif action == self.ACTIONS['DOWN']: new_y = min(self.env.GRID_SIZE-1,y+1)
        elif action == self.ACTIONS['LEFT']: new_x = max(0,x-1)
        if self.env.grid[new_y,new_x]==self.env.CELL_TYPES['WALL']:
            return {'x':x,'y':y}
        return {'x':new_x,'y':new_y}

    def update_epsilon(self):
        self.params['epsilon'] = max(self.params['epsilon_min'],
                                     self.params['epsilon']*self.params['epsilon_decay'])
