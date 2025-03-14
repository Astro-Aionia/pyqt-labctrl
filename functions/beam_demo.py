import os
import sys
sys.path.append('..')
sys.path.append('../instruments/toupcam')

from ui.beam_location_viewer_UI import Ui_beam_location
from functions.toupcam_demo import ToupDemo
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from calculation import circle_fit
import numpy as np

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class BeamLocation(ToupDemo, Ui_beam_location):
    def __init__(self, parent=None):
        ToupDemo.__init__(self, parent=parent)
        self.x = []
        self.y = []
        self.beam_pos = []
        self.canvas = MplCanvas()
        # self.toolbox = NavigationToolbar(self.canvas)
        vbox = QtWidgets.QVBoxLayout(self.widget)
        # vbox.addWidget(self.toolbox)
        vbox.addWidget(self.canvas)
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=10)
        self.pushButton_1.clicked.connect(lambda: self.clean())
        self.pushButton_2.clicked.connect(lambda: self.save_data())
    def acquire(self,path):
        if os.path.exists(path):
            super().acquire(path)
            self.beam_pos.append(circle_fit.circle_fit(circle_fit.get_border(circle_fit.get_binary(path))))
            print(self.beam_pos)
            self.x.append(self.counts)
            self.y.append(self.beam_pos[-1][1])
            print(self.x, self.y)
        else:
            print('No file in {path}'.format(path=path))
            return 'No file'
    def update_plot(self, i):
        self.canvas.ax.clear()
        self.canvas.ax.plot(self.x,self.y)
    def save_data(self):
        np.savetxt('beam.txt', self.beam_pos, delimiter=',')
    def clean(self):
        super().clean()
        self.x = []
        self.y = []
        self.beam_pos = []
        self.canvas.ax.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = BeamLocation()
    mainWindow.show()
    sys.exit(app.exec())