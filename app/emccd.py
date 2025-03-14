import sys
sys.path.append('..')
from ui.emccd_simple_UI import Ui_EMCCD
from ui.basic_control_panel_UI import Ui_basic_control_panel
from  ui.emccd_mainwindow import Ui_MainWindow
from functions.emccd_simple_control import LightFieldControlPanel
from functions.basic_control_panel import BasicControlPanel
import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.acq_instrument = LightFieldControlPanel()
        self.panel = BasicControlPanel(acq_instrument=self.acq_instrument)
        wid_1 = QtWidgets.QVBoxLayout(self.widget_1)
        wid_1.addWidget(self.panel)
        wid_2 = QtWidgets.QVBoxLayout(self.widget_2)
        wid_2.addWidget(self.acq_instrument)
    def closeEvent(self, a0: PyQt6.QtGui.QCloseEvent) -> None:
        self.acq_instrument.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())