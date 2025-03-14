import os
import sys
import time

from pyexpat.errors import messages

sys.path.append('..')
from instruments.emccd.lightfield import LightFieldSimplestApp
import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QDialog
from ui.emccd_simple_UI import Ui_EMCCD

import numpy
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QTextBrowser, QLineEdit
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel('Wavelength')
        plt.tight_layout()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)

class LightFieldControlPanel(LightFieldSimplestApp, QDialog, Ui_EMCCD):
    def __init__(self, parent=None, experiment: str = None, interface=True):
        LightFieldSimplestApp.__init__(self, experiment=experiment, interface=interface)
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.label_3.setText(self.get_dir())
        self.message = ''
        self.pushButton.clicked.connect(lambda : self.acquire(path="C:\\Users\\zhenggroup\\Python\\labctrl\\spectrum"))
        self.pushButton_2.clicked.connect(lambda : self.clean())
        self.data_canvas = MplCanvas()
        self.toolbox = NavigationToolbar(self.data_canvas)
        wid = QtWidgets.QVBoxLayout(self.widget)
        wid.addWidget(self.toolbox)
        wid.addWidget(self.data_canvas)
    def closeEvent(self, a0: PyQt6.QtGui.QCloseEvent) -> None:
        super().close()
    def acquire(self, path="C:\\Users\\zhenggroup\\Documents\\LightField"):
        self.label_3.setText(self.get_dir())
        data, self.message = super().acquire(path=path)
        self.update_plot(data)
        return self.message
    def update_plot(self, data):
        self.data_canvas.ax.clear()
        self.data_canvas.ax.plot(data[:,0],data[:,1])
        self.data_canvas.draw()
    def clean(self):
        super().clean()
        self.data_canvas.ax.clear()
        self.data_canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LightFieldControlPanel()
    mainWindow.show()
    sys.exit(app.exec())