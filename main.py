import sys
from PyQt6 import QtWidgets

sys.path.append(".\\instruments\\toupcam")
from ui.mainwindow_UI import Ui_MainWindow
from functions.basic_control_panel import BasicControlPanel
from functions.beam_location import BeamLocation
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.acq_instrument = BeamLocation()
        self.panel = BasicControlPanel(acq_instrument=self.acq_instrument)
        wid_1 = QtWidgets.QVBoxLayout(self.widget_1)
        wid_1.addWidget(self.panel)
        wid_2 = QtWidgets.QVBoxLayout(self.widget_2)
        wid_2.addWidget(self.acq_instrument)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())