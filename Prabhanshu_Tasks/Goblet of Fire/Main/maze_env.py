import pygame         #Will be used for rendering the Maze, Harry, Cup and the Death Eater.
import random         #For Randomly allocating a cell to Harry, Cup and Death Eater initially.
import numpy as np
from bfs import bfs   #For making the Death-Eater chase Harry using Breadth First Search Algorithm.
import math

#Defining Euclidian distance between two points for creating Distance based reward system:
def distance(a, b):
    return math.dist(a, b)

#Defining the Maze Cells-Size, Rows, Columns and Screen Size:
CELL_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 10
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE

class MazeEnv:                                #Creating the Class which contains the game-environment.
    def __init__(self, maze_file):            #Initialiazing the environment using given .txt files.
        self.maze = self.load_maze(maze_file) #Loading the maze layout into python.
        self.reset()                          #Resets the environment.
        self.action_space = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # possible actions : up, down, left, right.
        self.state_size = (MAZE_WIDTH, MAZE_HEIGHT)

    # loading the maze as a 2-D array of characters:
    def load_maze(self, filename):
        with open(filename, 'r') as f:
            lines = f.read().splitlines()                                      #Walls in the maze('X') are encoded as 1.
        maze = [[1 if char == 'X' else 0 for char in line] for line in lines]  #Free Space in maze is encoded as 0.
        return maze

    def reset(self):
        self.harry_pos = self.get_random_pos()
        self.cup_pos = self.get_random_pos()           #Randomly placed Harry,Cup and Death-Eater in the environment.
        self.de_pos = self.get_random_pos()
        while self.cup_pos == self.harry_pos or self.de_pos in [self.harry_pos, self.cup_pos]:
            self.cup_pos = self.get_random_pos()
            self.de_pos = self.get_random_pos()        #Ensuring that Harry,Cup and Death-Eater are in different cells int the new environment.
        return self.harry_pos

    def get_random_pos(self):                           #Alloting random position (x,y coordinates).
        while True:
            x = random.randint(0, MAZE_WIDTH-1)      #Choosing random coordinates in accordance with the maze size.
            y = random.randint(0, MAZE_HEIGHT-1)
            if self.maze[y][x] == 0:
                return (x, y)

    def step(self, action):                                         #Defining Step based on an action:
        old_harry_pos = self.harry_pos                              #Harry's Position before taking the action
        old_dist_de = distance(self.harry_pos, self.de_pos)         #Harry's distance from Death-Eater before action
        old_dist_cup = distance(self.harry_pos, self.cup_pos)       #Harry's distance from Cup before action
        dx, dy = action
        new_x = self.harry_pos[0] + dx
        new_y = self.harry_pos[1] + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and self.maze[new_y][new_x] == 0:
            self.harry_pos = (new_x, new_y)                         #Harry's position after taking action if action is possible

        self.de_pos = bfs(self.maze, self.de_pos, self.harry_pos)   #Position of Death-Eater after taking a step towards Harry using BFS Algorithm.
        new_dist_de = distance(self.harry_pos, self.de_pos)         #Harry's distance from Death-Eater after action
        new_dist_cup = distance(self.harry_pos, self.cup_pos)       #Harry's distance from Cup after action

        done = False                                                #This denotes that the process of taking steps is not terminated.
        reward = -1                                                 #Penalising every step : This will prevent agent from taking extra steps than required.

        if self.harry_pos == self.cup_pos:
            reward = 100                                            #Giving high reward on catching the Cup.
            done = True                                             #To finish the episode since Harry got the Cup.
        elif self.harry_pos == self.de_pos:
            reward = -100                                           #Heavily penalising the agent for getting caught by Death-Eater
            done = True                                             #To finish the episode since Harry was caught by the Death-Eater
        else:
              if new_dist_de > old_dist_de:
                 reward += 5                                         #Awarding the agent for getting away from Death-Eater
              else:
                 reward -= 5                                        #Penalising the agent for getting close to Death-Eater
              if new_dist_cup < old_dist_cup:
                reward += 10                                         #Awarding the agent for getting close to Cup.
              else:
                reward -= 10                                         #Penalising the agent for getting away from Cup.
        return self.harry_pos, reward, done

    def render(self, screen):
        colors = {
            'wall': (40, 40, 40),
            'floor': (255, 255, 255),
            'harry': (0, 0, 255),
            'cup': (255, 215, 0),
            'de': (255, 0, 0)
        }
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                color = colors['wall'] if self.maze[y][x] == 1 else colors['floor']
                pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))           #Drawing the Maze using PyGame.
        pygame.draw.rect(screen, colors['cup'], (*[c * CELL_SIZE for c in self.cup_pos], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, colors['harry'], (*[c * CELL_SIZE for c in self.harry_pos], CELL_SIZE, CELL_SIZE))   #Drawing cup, harry and death-eater.
        pygame.draw.rect(screen, colors['de'], (*[c * CELL_SIZE for c in self.de_pos], CELL_SIZE, CELL_SIZE))
