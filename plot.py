import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np


class Plot:

    def __init__(self, title, x_label, y_label, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        '''
        plt.plot(self.x_data, self.y_data)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(True)
        '''
        self.fig = plt.gcf()
        self.fig.show()
        self.fig.canvas.draw()
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(True)


    def addData(self, x, y):
        self.x_data = np.append(self.x_data, x)
        self.y_data = np.append(self.y_data, y)


    def plot(self):
        plt.plot(self.x_data, self.y_data)
        self.fig.canvas.draw()


