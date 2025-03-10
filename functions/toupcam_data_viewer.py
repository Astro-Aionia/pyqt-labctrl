import os
import sys
sys.path.append('..')
sys.path.append('../instruments/toupcam')
import time
# from ui.toupcam_data_viewer_UI import Ui_toupcam_data_viewer
from ui.beam_location_UI import Ui_beam_location
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QPixmap
from instruments.toupcam.camera import ToupCamCamera

class ToupAccquire(QDialog, Ui_beam_location):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.cam = ToupCamCamera()
        self.cam.open()
        time.sleep(2)
        self.counts = 0
    def __del__(self):
        self.cam.close()
        time.sleep(2)
    def acquire(self, path):
        self.cam.save_tiff(path)
        time.sleep(2)
        self.counts = self.counts + 1
        if os.path.exists(path):
            self.label_1.setPixmap(QPixmap(path).scaled(self.label.size()))
            self.label.repaint()
            return path
        else:
            print('No file in {path}'.format(path=path))
            return 'No file'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ToupAccquire()
    mainWindow.show()
    sys.exit(app.exec())