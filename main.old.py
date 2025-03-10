import sys

from PyQt6.uic.properties import QtCore

sys.path.append(".\\instruments\\toupcam")
import os
import time
from time import sleep

from ui.main_gui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt6.QtGui import QPixmap

import serial
from instruments.servo_stage.servo import Servo
from instruments.toupcam.camera import ToupCamCamera

import numpy as np
from canvas.mpl import AnimationWidget
from calculation import circle_fit


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.servo = Servo(port="COM1")
        self.cam = ToupCamCamera()
        self.initialize()
        self.position = 0
        self.displacement = 0
        self.velocity = float(self.lineEdit_6.text())
        self.move_abs()
        self._photo_num = 0
        self.beam_position = []

        self.pushButton.clicked.connect(lambda: self.acquire_listfile())
        self.pushButton_1.clicked.connect(lambda: self.move_pos())
        self.pushButton_2.clicked.connect(lambda: self.move_neg())
        self.pushButton_3.clicked.connect(lambda: self.move_abs())
        self.pushButton_4.clicked.connect(lambda: self.acquire())
        self.pushButton_5.clicked.connect(lambda:self.acquire_list())

        self.ani = AnimationWidget(width=6, height=3.4, dpi=100)
        self.verticalLayout_3.addWidget(self.ani)

    def initialize(self):
        self.lineEdit.setText('0')
        self.lineEdit_1.setText('0')
        self.lineEdit_2.setText('0')
        self.lineEdit_3.setText('0')
        self.lineEdit_4.setText('0')
        self.lineEdit_5.setText('.\delay.txt')
        self.lineEdit_6.setText('30')
        self.label_16.setScaledContents(True)
    def set_vel(self):
        self.velocity = float(self.lineEdit_6.text())
        self.textEdit.append("Velocity set to {vel}".format(vel=self.velocity))
    def move_abs(self):
        self.displacement = abs(self.position - float(self.lineEdit_2.text()))
        self.position = float(self.lineEdit_2.text())
        self.servo.connect()
        self.textEdit.append("Moving to {pos} mm...".format(pos=self.position))
        QApplication.processEvents()
        self.servo.moveabs(pos=self.position,vel=self.velocity,sleep=self.displacement/self.velocity)
        self.textEdit.append("Done.")
        self.servo.disconnect()
    def move_pos(self):
        self.displacement = abs(float(self.lineEdit_1.text()))
        self.servo.connect()
        self.textEdit.append("Moving by +{dis} mm...".format(dis=self.displacement))
        QApplication.processEvents()
        self.servo.moveinc(pos=self.displacement, vel=self.velocity, sleep=self.displacement / self.velocity)
        self.position = self.position + self.displacement
        self.textEdit.append("Done.")
        self.servo.disconnect()
    def move_neg(self):
        self.displacement = abs(float(self.lineEdit_1.text()))
        self.servo.connect()
        self.textEdit.append("Moving by -{dis} mm...".format(dis=self.displacement))
        QApplication.processEvents()
        self.servo.moveinc(pos=-self.displacement, vel=self.velocity, sleep=self.displacement / self.velocity)
        self.position = self.position - self.displacement
        self.textEdit.append("Done.")
        self.servo.disconnect()
    def acquire(self, filename=''):
        path = ".\\photos\\" + str(self._photo_num).zfill(5) + filename + '.tif'
        # self.cam.open()
        # time.sleep(2)
        # self.cam.save_tiff(path)
        # time.sleep(2)
        # self.cam.close()
        self.textEdit.append("Saved in "+path)
        self._photo_num = self._photo_num + 1
        self.show_photo(path=path)
        return path
    def acquire_list(self):
        delaylist = np.arange(float(self.lineEdit.text()),float(self.lineEdit_3.text()), float(self.lineEdit_4.text()))
        for pos in delaylist:
            self.lineEdit_2.setText(str(pos))
            self.move_abs()
            path = self.acquire(filename='_position{pos}'.format(pos=str(pos)))
            self.ani.ani_update(x=pos, y=self.calc_pos(path)[1])
            self.save_beam_position()
    def acquire_listfile(self):
        file = self.lineEdit_5.text()
        if os.path.exists(file):
            delaylist = np.loadtxt(file)
            for pos in delaylist:
                self.lineEdit_2.setText(str(pos))
                self.move_abs()
                path = self.acquire(filename='_position{pos}'.format(pos=str(pos)))
                self.ani.get_data(x=pos, y=self.calc_pos(path)[1])
                self.save_beam_position()
        else:
            self.textEdit.append("File not exist.")
    def show_photo(self, path):
        pixmap = QPixmap(path)
        # scaled(self.label_16.width(), self.label_16.height(), QtCore.Qt.KeepAspectRatio)
        self.label_16.setPixmap(pixmap)
        self.label_16.repaint()
        QApplication.processEvents()
    def calc_pos(self, path):
        beam = circle_fit.circle_fit(circle_fit.get_border(circle_fit.get_binary(path)))
        self.beam_position.append(beam)
        return beam
    def save_beam_position(self):
        np.savetxt('curve.csv', self.beam_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())