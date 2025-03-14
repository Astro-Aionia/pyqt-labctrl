#! /usr/bin/env python3
# coding: utf-8

import sys
import os
import random

import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QTextBrowser, QLineEdit
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(1, 1, 1)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.main_widget = QtWidgets.QWidget(self)
        self.xs = []
        self.ys = []
        vbox = QtWidgets.QVBoxLayout(self.main_widget)

        self.canvas = MyMplCanvas(self.main_widget, width=6, height=6, dpi=100)  ###attention###
        vbox.addWidget(self.canvas)

        hbox = QtWidgets.QHBoxLayout(self.main_widget)
        self.textBrowser = QTextBrowser(self)
        self.lineEdit = QLineEdit(self)

        vbox.addWidget(self.textBrowser)
        vbox.addWidget(self.lineEdit)

        self.setLayout(vbox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.lineEdit.returnPressed.connect(self.update_text)

        self.ani = FuncAnimation(self.canvas.figure, self.update_line, interval=10)

    def update_line(self, i):
        self.canvas.ax.clear()
        self.canvas.ax.plot(self.xs, self.ys)

    def update_text(self):
        self.text = self.lineEdit.text()
        self.textBrowser.append(self.text)
        x, y = self.text.split(',')
        self.xs.append(float(x))
        self.ys.append(float(y))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    App.exit()
    sys.exit(App.exec())
