import random
import numpy as np
import math
from maze import Maze
from utils import build_empty_matrix
import itertools

dl = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


class QLearning:
    def __init__(self, maze: Maze):
        self.R = build_empty_matrix(maze.n, maze.n)
        # lista = [i for i in range(0, maze.n)]
        # states = list(itertools.product(lista, lista))
        self.Q = np.zeros((maze.n, maze.n, 4))
        self.maze = maze
        for i in range(0, maze.n):
            for j in range(0, maze.n):
                if maze.table[i][j] is 'N' or maze.table[i][j] is 'S':
                    self.R[i][j] = -0.4
                elif maze.table[i][j] is 'X':
                    self.R[i][j] = -math.inf
                elif maze.table[i][j] is 'W':
                    self.R[i][j] = 1000.0
                else:
                    self.R[i][j] = -1000.0
        self.R = np.asarray(self.R)

    def train(self, epochs=100, eta=0.1, gamma=0.2, exploration_rate=0.1):
        for no_epoch in range(0, epochs):
            self.state = tuple(self.maze.start)
            # cat timp n-am win/lose state
            while True:
                if random.uniform(0, 1) <= exploration_rate:
                    # fac explorare
                    action = self.get_random_action(self.state)
                else:
                    action = self.get_best_action(self.state)
                next_state, reward = self.take_action(action)

                max_next_Q = max([self.Q[next_state][k] for k in range(0, 4)])
                # update la Q
                self.Q[self.state][action] = self.Q[self.state][action] + eta * \
                    (reward + gamma * max_next_Q - self.Q[self.state][action])

                self.state = next_state
                value = self.maze.table[self.state[0]][self.state[1]]
                if value is 'W' or value is 'L':
                    break

            print(f'Finished epoch {no_epoch}')

    def solve(self):
        print('\n\n')
        print(self.maze)
        print('Predicting where I should go')
        self.state = self.maze.start
        while True:
            print(self.state)
            value = self.maze.table[self.state[0]][self.state[1]]
            if value is 'W' or value is 'L':
                break
            action = self.get_best_action(self.state)
            next_state, _ = self.take_action(action)
            self.state = next_state

    def take_action(self, action):
        next_state = (self.state[0] + dl[action], self.state[1] + dc[action])
        reward = self.R[next_state]
        return next_state, reward

    def get_best_action(self, state):
        q_values = []
        actions = []
        lin, col = state
        for k in range(0, 4):
            if self.state_is_possible((lin + dl[k], col + dc[k])):
                q_values.append(self.Q[state][k])
            else:
                q_values.append(-math.inf)
        max_q = max(q_values)
        for index, value in enumerate(q_values):
            if value == max_q:
                actions.append(index)
        return random.choice(actions)

    def get_random_action(self, state):
        actions = []
        lin, col = state
        for k in range(0, 4):
            if self.state_is_possible((lin + dl[k], col + dc[k])):
                actions.append(k)
        return random.choice(actions)

    def state_is_possible(self, state):
        lin, col = state
        if lin < 0 or lin >= self.maze.n:
            return False
        if col < 0 or col >= self.maze.n:
            return False
        if self.maze.table[lin][col] == 'X':
            return False
        return True

    def get_next_state(self, state):
        return random.choice(self.get_next_states(state))

    def get_next_states(self, state):
        possibilities = []
        lin, col = state
        for k in range(0, 4):
            if lin + dl[k] < 0 or lin + dl[k] >= self.maze.n:
                continue
            if col + dc[k] < 0 or col + dc[k] >= self.maze.n:
                continue
            if self.maze[lin + dl[k]][col + dc[k]] != 'X':
                next_state = (lin+dl[k], col + dc[k])
                next_action = k
                possibilities.append(next_state, next_action)

        return possibilities
