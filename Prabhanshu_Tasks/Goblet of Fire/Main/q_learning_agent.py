import numpy as np
import random

class QLearningAgent:                                               #Contains the behavior of Q-Learning Agent
    def __init__(self, state_size,  actions, alpha=1.0, alpha_decay=0.999, alpha_min = 0.05, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.q_table = {}                              #Initialises q table as an empty dictionary. It will have 'keys' as states and 'values' as numpy array of q values for each action.
        self.actions = actions                         #Stores the list of possible actions from that state.
        self.alpha = alpha                             #Learning Rate of the agent(alpha) is high in the beginning(1.0).
        self.alpha_decay = alpha_decay                 #alpha decays gradually until it reaches a minimum(0.05).
        self.alpha_min = alpha_min
        self.gamma = gamma
        self.epsilon = epsilon                         #In the beginning, the tendency to explore is high(epsilon=1.0)
        self.epsilon_decay = epsilon_decay             #Gradually, epsilon decays as the agent learns to catch the cup escaping the death-eaters.
        self.epsilon_min = epsilon_min

    def get_q(self, state):                             #If the state is not in the q-table, it initialises a new array of zeros for this state.
        return self.q_table.setdefault(state, np.zeros(len(self.actions)))

    def choose_action(self, state):                         #Selection of an action using epsilon-greedy strategy:
        if random.random() < self.epsilon:                  #Exploration : Choose a random no. between 0 and 1 and checks if it is less than epsilon:
            return random.choice(self.actions)                              #Returns a random action from (up,down,left,right)
        return self.actions[np.argmax(self.get_q(state))]   #Exploitation : Returns the action with highest q value.

    def update(self, state, action, reward, next_state):    #Updating the Q-Table for the current state and actions
        action_idx = self.actions.index(action)
        current_q = self.get_q(state)[action_idx]           #Retrieves the current q-value of the state.
        max_next_q = np.max(self.get_q(next_state))         #Finding maximum q-value in the next state.
        self.q_table[state][action_idx] += self.alpha * (reward + self.gamma * max_next_q - current_q) #Using Q-Value update formula.
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.alpha = max(self.alpha_min, self.alpha_decay * self.alpha)
