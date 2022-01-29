import pandas as pd
import PyQt5
from PyQt5 import QtWidgets, uic
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from vituix_converter_UI import (Ui_MainWindow)


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_hats.clicked.connect(hats_conversion)
        self.show()

    def hats_conversion(self):



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MyMainWindow()
    sys.exit(app.exec_())
