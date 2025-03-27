import os
import sys
sys.path.append('..')
from instruments.topas.topas import Topas
import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QDialog
from ui.topas_UI import Ui_topas

class TopasControlPanel(Topas, QDialog, Ui_topas):
    def __init__(self, serialNumber, parent=None):
        Topas.__init__(self, serialNumber=serialNumber)
        if self.topas is None:
            return
        else:
            QDialog.__init__(self, parent=parent)
            self.setupUi(self)
            print(self.interaction)
            print(self.wavelength)
            self.pushButton.toggle()
            self.lineEdit_1.setReadOnly(True)
            self.lineEdit_1.setText(str(int(self._interactions[self.interaction][0])))
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit_2.setText(str(int(self._interactions[self.interaction][1])))
            self.lineEdit_3.setText(str(self.wavelength))
            self._cblist = []
            for i in range(self.comboBox.count()):
                self._cblist.append(self.comboBox.itemText(i))
            self.comboBox.setCurrentIndex(self._cblist.index(self.interaction))
            self.comboBox.currentIndexChanged.connect(lambda: self.set_interaction(self.comboBox.currentText()))
            self.lineEdit_3.editingFinished.connect(lambda: self.set_wavelength((float(self.lineEdit_3.text()))))
            self.pushButton.clicked.connect(lambda: self.changeShutter())

    def set_interaction(self, interaction):
        if super().set_interaction(interaction):
            self.textEdit.append(f"Interaction set to {interaction}.")
            self.lineEdit_1.setText(str(int(self._interactions[self.interaction][0])))
            self.lineEdit_2.setText(str(int(self._interactions[self.interaction][1])))
        else:
            self.textEdit.append(f"Not such a interaction named {interaction}.")
    def set_wavelength(self, wavelength):
        self.textEdit.append(f"Wavelength is setting to {wavelength}...")
        if super().set_wavelength(wavelength):
            self.textEdit.append(f"Wavelength set to {wavelength}.")
        else:
            self.textEdit.append(f"Wavelength {wavelength} is out of range.")
            self.lineEdit_3.setText(str(self.wavelength))
    def changeShutter(self):
        super().changeShutter()
        if self.shutter:
            self.textEdit.append("Now shutter is open.")
        else:
            self.textEdit.append("Now shutter is closed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = TopasControlPanel(serialNumber="T23231P")
    mainWindow.show()
    sys.exit(app.exec())