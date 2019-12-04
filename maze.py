import random


class Maze:
    def __init__(self, n=10, no_obstacles=3):
        self.n = n
        self.no_obstacles = no_obstacles
        self.generate_maze()

    def __str__(self):
        res = ''
        for i in range(0, self.n):
            for j in range(0, self.n):
                res += str(self.table[i][j]) + ' '
            res += '\n'
        return res

    def generate_maze(self):
        self.table = [None] * self.n
        for i in range(0, self.n):
            self.table[i] = ['N'] * self.n
        # generam obstacole
        self.obstacles = []
        for i in range(0, self.no_obstacles):
            while True:
                lin = random.randint(0, self.n - 1)
                col = random.randint(0, self.n - 1)
                if (self.does_not_have_neighbour_obstacle(lin, col) and self.table[lin][col] == 'N'):
                    self.table[lin][col] = 'X'
                    self.obstacles.append((lin, col))
                    break
        # generate start, win and lose
        values = ['S', 'W', 'L']
        for value in values:
            while True:
                lin = random.randint(0, self.n - 1)
                col = random.randint(0, self.n - 1)
                if self.does_not_have_neighbour_obstacle(lin, col) and self.table[lin][col] == 'N':
                    self.table[lin][col] = value
                    if value is 'S':
                        self.start = (lin, col)
                    elif value is 'W':
                        self.win = (lin, col)
                    else:
                        self.lose = (lin, col)
                    break

    def does_not_have_neighbour_obstacle(self, lin, col):
        dl = [-1, -1, 0, 1, 1, 1, 0, -1]
        dc = [0, 1, 1, 1, 0, -1, -1, -1]
        for k in range(0, 8):
            if lin + dl[k] < 0 or lin + dl[k] >= self.n:
                continue
            if col + dc[k] < 0 or col + dc[k] >= self.n:
                continue
            if self.table[lin + dl[k]][col + dc[k]] is 'X':
                return False
        return True
