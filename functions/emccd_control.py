import os
import sys
sys.path.append('..')
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
from instruments.emccd.lightfield import LightFieldApp
import clr
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# Import System.IO for saving and opening files
from System.IO import *
# Import c compatible List and String
from System import String
from System.Collections.Generic import List

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import DeviceType, ExperimentSettings, CameraSettings, RegionOfInterest, AdcQuality, SpectrometerSettings

import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QDialog
from ui.emccd_UI import Ui_EMCCD
from file_dialog import FileSelect

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class LightFieldControlPanel(LightFieldApp, QDialog, Ui_EMCCD):
    def __init__(self, parent=None, experiment: str = None, interface=True):
        LightFieldApp.__init__(self, experiment=experiment, interface=interface)
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.experiment_setup_bar = FileSelect(filter_=str("LightField experiment files (*.lfe)"))
        self.save_path_bar = FileSelect(mode=QtWidgets.QFileDialog.FileMode.Directory)
        self.data_view_bar = FileSelect(filter_=str("Spectrum files files (*.spe)"))
        vbox_1 = QtWidgets.QVBoxLayout(self.FileDialog_1)
        vbox_2 = QtWidgets.QVBoxLayout(self.FileDialog_2)
        vbox_3 = QtWidgets.QVBoxLayout(self.FileDialog_3)
        vbox_1.addWidget(self.experiment_setup_bar)
        vbox_2.addWidget(self.save_path_bar)
        vbox_3.addWidget(self.data_view_bar)
        self.refresh()
    def closeEvent(self, a0: PyQt6.QtGui.QCloseEvent) -> None:
        super().close()
    def get_value(self, setting):
        if self.experiment.Exists(setting):
            return str(self.experiment.GetValue(setting))
        else:
            print(f"{setting} is not a valid setting.")
    def refresh(self):
        self.lineEdit.setText(self.get_value(ExperimentSettings.AcquisitionFramesToStore))
        self.lineEdit_3.setText(self.get_value(CameraSettings.ShutterTimingExposureTime))
        self.lineEdit_4.setText(self.get_value(CameraSettings.AdcSpeed))
        self.lineEdit_5.setText(self.get_value(SpectrometerSettings.GratingCenterWavelength))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = LightFieldControlPanel()
    mainWindow.show()
    sys.exit(app.exec())