import os
import sys
sys.path.append('..')
from ui.basic_control_panel_UI import Ui_basic_control_panel
from functions.file_dialog import FileSelect
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog
from instruments.servo_stage.servo import Servo
import numpy as np

class AcquireNone():
    def __init__(self):
        self.counts = 0
    def acquire(self, path):
        self.counts = self.counts + 1
        return self.counts
    def show(self):
        pass
    def acquire_show(self):
        self.acquire()
        self.show()

class BasicControlPanel(QDialog, Ui_basic_control_panel):
    def __init__(self, parent=None, acq_instrument = AcquireNone()):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.lineEdit_1.setText('0')
        self.lineEdit_2.setText('0')
        self.lineEdit_3.setText('0')
        self.lineEdit_4.setText('0')
        self.lineEdit_5.setText('0')
        self.lineEdit_6.setText('30')
        self.servo = Servo(port="COM8")
        self.position = 0
        self.displacement = 300
        self.velocity = float(self.lineEdit_6.text())
        self.save_path = "C:\\Users\\zhenggroup\\Python\\labctrl\\photos"
        self.move_abs()
        # self._acquire_num = 0
        # self.beam_position = []
        self.acq_instrument = acq_instrument

        fd_1 = QtWidgets.QVBoxLayout(self.fileDialog_1)
        self.fileSelcet_1 = FileSelect()
        fd_1.addWidget(self.fileSelcet_1)
        fd_2 = QtWidgets.QVBoxLayout(self.fileDialog_2)
        self.fileSelcet_2 = FileSelect(mode=QtWidgets.QFileDialog.FileMode.Directory)
        self.fileSelcet_2.lineEdit.setText(self.save_path)
        fd_2.addWidget(self.fileSelcet_2)

        self.pushButton_1.clicked.connect(lambda: self.move_pos())
        self.pushButton_2.clicked.connect(lambda: self.move_neg())
        self.pushButton_3.clicked.connect(lambda: self.move_abs())
        self.pushButton_4.clicked.connect(lambda: self.acquire())
        self.pushButton_5.clicked.connect(lambda: self.acquire_list())
        self.pushButton_6.clicked.connect(lambda: self.acquire_listfile())
        self.lineEdit_6.editingFinished.connect(lambda: self.set_vel())
        self.fileSelcet_2.lineEdit.textChanged.connect(lambda: self.get_save_path())

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
    def get_save_path(self):
        path = self.fileSelcet_2.lineEdit.text()
        new_path = path.replace('/', '\\')
        self.save_path = new_path
        print(new_path)
    def acquire(self, filename=''):
        self.acq_instrument.acquire(self.save_path)
        self.textEdit.append("Saved in "+self.save_path)
    def acquire_list(self):
        delaylist = np.arange(float(self.lineEdit_3.text()),float(self.lineEdit_4.text()), float(self.lineEdit_5.text()))
        for pos in delaylist:
            self.lineEdit_2.setText(str(pos))
            self.move_abs()
            self.acquire(filename='_position{pos}'.format(pos=str(pos)))
    def acquire_listfile(self):
        file = self.fileSelcet_1.lineEdit.text()
        if os.path.exists(file):
            delaylist = np.loadtxt(file)
            for pos in delaylist:
                self.lineEdit_2.setText(str(pos))
                self.move_abs()
                self.acquire(filename='_position{pos}'.format(pos=str(pos)))
        else:
            self.textEdit.append("File not exist in {path}.".format(path=file))

if __name__ == '__main__':
    acp_ins = AcquireNone()
    app = QApplication(sys.argv)
    mainWindow = BasicControlPanel(acq_instrument=acp_ins)
    mainWindow.show()
    sys.exit(app.exec())