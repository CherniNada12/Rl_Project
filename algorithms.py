import numpy as np

class QLearning:
    @staticmethod
    def update(agent, state, action, reward, next_state):
        s = f"{state['x']},{state['y']}"
        ns = f"{next_state['x']},{next_state['y']}"
        if s not in agent.q_table: return
        current_q = agent.q_table[s][action]
        max_next = max(agent.q_table.get(ns,[0]*4))
        agent.q_table[s][action] = current_q + agent.params['alpha']*(reward + agent.params['gamma']*max_next - current_q)

class DoubleQLearning:
    @staticmethod
    def update(agent,state,action,reward,next_state):
        s=f"{state['x']},{state['y']}"
        ns=f"{next_state['x']},{next_state['y']}"
        if s not in agent.q_table or s not in agent.q_table2: return
        if np.random.random()<0.5:
            current_q = agent.q_table[s][action]
            best_action = np.argmax(agent.q_table[ns])
            next_q = agent.q_table2[ns][best_action]
            agent.q_table[s][action] = current_q + agent.params['alpha']*(reward+agent.params['gamma']*next_q - current_q)
        else:
            current_q = agent.q_table2[s][action]
            best_action = np.argmax(agent.q_table2[ns])
            next_q = agent.q_table[ns][best_action]
            agent.q_table2[s][action] = current_q + agent.params['alpha']*(reward+agent.params['gamma']*next_q - current_q)

class SARSA:
    @staticmethod
    def update(agent,state,action,reward,next_state,next_action):
        s=f"{state['x']},{state['y']}"
        ns=f"{next_state['x']},{next_state['y']}"
        if s not in agent.q_table: return
        current_q = agent.q_table[s][action]
        next_q = agent.q_table[ns][next_action]
        agent.q_table[s][action] = current_q + agent.params['alpha']*(reward+agent.params['gamma']*next_q - current_q)
