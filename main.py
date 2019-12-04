from maze import Maze
from q_learning import QLearning

if __name__ == '__main__':
    maze = Maze(n=10, no_obstacles=5)
    q_learning = QLearning(maze)
    q_learning.train(epochs=1000, eta=1.5, gamma=0.1, exploration_rate=0.1)
    q_learning.solve()
