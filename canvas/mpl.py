import sys
from PyQt6 import QtWidgets

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from numpy.ma.core import append


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=600):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
    def compute_initial_figure(self):
        pass

class AnimationWidget(QtWidgets.QWidget):
    def __init__(self, width=5, height=4, dpi=600):
        QtWidgets.QWidget.__init__(self)
        vbox = QtWidgets.QVBoxLayout()
        self.canvas = MplCanvas(self, width=width, height=height, dpi=dpi)
        self.toolbar = NavigationToolbar(self.canvas)
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)
        self.x = [0,0.1]
        self.y = [0,0]
        self.plot, = self.canvas.axes.plot(self.x, self.y, 'bo', animated=True, lw=2)
        self.ani = FuncAnimation(self.canvas.figure, self.get_data(None, None))

    def get_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.plot.set_xdata(self.x)
        self.plot.set_ydata(self.y)
        self.plot, = self.canvas.axes.plot(self.x, self.y, 'bo', animated=True, lw=2)
        return self.x, self.y

    def ani_update(self, x, y):
        self.ani = FuncAnimation(self.canvas.figure, self.get_data(x, y))