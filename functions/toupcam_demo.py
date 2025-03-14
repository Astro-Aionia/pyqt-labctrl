import os
import sys
sys.path.append('..')

from ui.beam_location_viewer_UI import Ui_beam_location
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6.QtGui import QPixmap

class ToupDemo(QDialog, Ui_beam_location):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.counts = 0
        # self.label.setPixmap(QPixmap('..\\photos\\00000_position0.0.tif').scaled(self.label.size()))
        # self.label.repaint()
    def acquire(self, path):
        if os.path.exists(path):
            self.counts = self.counts + 1
            self.label_2.setPixmap(QPixmap(path).scaled(self.label_2.size()))
            self.label_2.repaint()
            return path
        else:
            print('No file in {path}'.format(path=path))
            return 'No file'
    def clean(self):
        self.counts = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ToupDemo()
    mainWindow.show()
    sys.exit(app.exec())