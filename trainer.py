import numpy as np
from collections import deque
from algorithms import QLearning, DoubleQLearning, SARSA

class Trainer:
    def __init__(self, environment, agent, max_steps=100):
        self.env = environment
        self.agent = agent
        self.max_steps = max_steps
        self.training_stats = deque(maxlen=100)
        self.episode = 0
        self.algorithms = {'qlearning':QLearning,'doubleq':DoubleQLearning,'sarsa':SARSA}

    def train_episode(self, algorithm='qlearning'):
        state = self.env.start_position.copy()
        episode_reward = 0
        steps = 0
        action = self.agent.choose_action(state['x'],state['y'])
        while steps < self.max_steps:
            next_state = self.agent.get_next_state(state['x'],state['y'],action)
            reward = self.env.get_reward(next_state['x'],next_state['y'])
            episode_reward += reward
            next_action = self.agent.choose_action(next_state['x'],next_state['y'])
            algo = self.algorithms[algorithm]
            if algorithm=='sarsa':
                algo.update(self.agent,state,action,reward,next_state,next_action)
            else:
                algo.update(self.agent,state,action,reward,next_state)
            if self.env.is_terminal(next_state['x'],next_state['y']): break
            state=next_state
            action=next_action
            steps+=1
        self.agent.update_epsilon()
        success = self.env.get_cell_type(state['x'],state['y'])==self.env.CELL_TYPES['TREASURE']
        result={'reward':episode_reward,'steps':steps,'success':success}
        self.training_stats.append(result)
        self.episode+=1
        return result

    def get_statistics(self):
        if not self.training_stats: return {'episode':0,'epsilon':1.0,'success_rate':0,'avg_reward':0,'avg_steps':0}
        success_count = sum(1 for r in self.training_stats if r['success'])
        avg_reward = np.mean([r['reward'] for r in self.training_stats])
        avg_steps = np.mean([r['steps'] for r in self.training_stats])
        success_rate = success_count/len(self.training_stats)*100
        return {'episode':self.episode,'epsilon':self.agent.params['epsilon'],
                'success_rate':success_rate,'avg_reward':avg_reward,'avg_steps':avg_steps}

    def reset(self):
        self.agent.reset_q_tables()
        self.training_stats.clear()
        self.episode = 0
