# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

BACKGROUND_IMAGE_PATH = '/media/psf/Home/UbuntuShare/Program/python/test_and_tools/resource/flag_wide.jpg'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.background = QLabel('', self)
        self.background_image = None
        self.close_button = QPushButton('Quit', self)
        self.init()

    def init(self):
        self.close_button.clicked.connect(QCoreApplication.quit)
        self.close_button.setGeometry(QRect(30, 500, 30, 30))
        self.background_image = QPixmap(BACKGROUND_IMAGE_PATH)

    def resizeEvent(self, event):
        size = self.size()
        w, h = size.width(), size.height()
        background_image = self.background_image.scaled(w, h)
        self.background.setPixmap(background_image)
        self.background.setAutoFillBackground(True)
        self.background.setGeometry(QRect(0, 0, w, h))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    window.showFullScreen()
    sys.exit(app.exec_())
