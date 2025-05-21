import pygame
import numpy as np
from maze_env import MazeEnv
from q_learning_agent import QLearningAgent

def evaluate_model(env, agent, episodes=100, render=False):    #Defining a function to evaluate the trained agent.
    successes = 0
    agent.epsilon = 0  # Turn off exploration during evaluation for ONLY exploitation

    pygame.init()
    screen = pygame.display.set_mode((env.state_size[0]*40, env.state_size[1]*40))

    for ep in range(episodes):
        state = env.reset()
        done = False
        steps = 0
        while not done and steps < 50:
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                env.render(screen)
                pygame.display.flip()
                pygame.time.delay(100)

            action = agent.choose_action(state)     #Agent chooses the best action (epsilon = 0, so always exploits).
            next_state, reward, done = env.step(action)
            state = next_state
            steps+=1

        if reward == 100:
            successes += 1
        print(f"Test Episode {ep+1}: {'Success' if reward == 100 else 'Caught'}")

    pygame.quit()
    print(f"\n Success Rate: {successes}/{episodes} = {successes / episodes * 100:.2f}%")

if __name__ == "__main__":
    env = MazeEnv('V1.txt')
    agent = QLearningAgent(env.state_size, env.action_space)
    agent.q_table = np.load("trained_q_table.npy", allow_pickle=True).item()
    evaluate_model(env, agent, episodes=100, render=True)