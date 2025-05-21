import pygame
import matplotlib.pyplot as plt
from maze_env import MazeEnv
from q_learning_agent import QLearningAgent
import numpy as np

EPISODES = 100000                           #Higher Number of Episodes help the agent to better learn the optimal policy.
env = MazeEnv('V1.txt')                                         #creating the maze environment
agent = QLearningAgent(env.state_size, env.action_space)        #Creating a q-learning agent(Harry) in the maze environment

pygame.init()           #initialising the PyGame window with desired screen size :
screen = pygame.display.set_mode((env.state_size[0]*40, env.state_size[1]*40))

rewards, successes = [], []         #The rewards list stores the total reward earned by the agent in each episode.

for e in range(EPISODES):
    steps = 0                       #Initialising steps taken by Harry in each episode.
    state = env.reset()             #Resets the Maze environment in the beginning of each episode.
    total_reward = 0                #Initialising the total reward earned in each episode.
    done = False
    while not done and steps < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                               #To quit the PyGame window on User's call.
        action = agent.choose_action(state)                 #Agent chooses an action based on epsilon-greedy policy.
        next_state, reward, done = env.step(action)         #On basis of the action chosen, agent comes to the next state and gets some reward.
        agent.update(state, action, reward, next_state)     #Agent updates its Q-table using the reward and the new state.
        total_reward += reward
        state = next_state                                  #updating the state
        env.render(screen)                                  #Displays the current maze state on the screen using pygame.
        pygame.display.flip()
        steps += 1
    rewards.append(total_reward)                            #Storing the total reward for the episode.
    successes.append(1 if reward > 0 else 0)                #Stores 1 in success list if Harry taking the cup terminates the loop, else 0.
    # print(f"Episode {e+1}, Reward: {total_reward}, Success: {reward > 0}")

pygame.quit()
np.save("trained_q_table.npy", agent.q_table)           #Saving the q_table after complete training of the agent.

plt.plot(rewards, label='Episode Reward')
plt.plot(np.convolve(successes, np.ones(10)/10, mode='valid'), label='Success Rate (10 avg)')
plt.legend()
plt.show()