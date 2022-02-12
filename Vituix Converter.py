import os
import shutil
import sys

import pandas as pd
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *

from vituix_converter_UI import (Ui_MainWindow)


def no_file_selected():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowIcon(QtGui.QIcon("D:/Python Projects/HATS SAMS Conversion/Icon/Vituix_Converter_Icon_R1.ico"))
    msg.setText("No File Was Selected!")
    msg.setWindowTitle("Warning!")
    retval = msg.exec_()


def process_completed():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QtGui.QIcon("D:/Python Projects/HATS SAMS Conversion/Icon/Vituix_Converter_Icon_R1.ico"))
    msg.setText("Files are converted.")
    msg.setWindowTitle("Completed!")
    retval = msg.exec_()


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_hats.clicked.connect(self.hats_conversion)
        self.pushButton_sams.clicked.connect(self.sams_conversion)
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.viewport().installEventFilter(self)
        types = ['text/uri-list']
        types.extend(self.tableWidget.mimeTypes())
        self.tableWidget.mimeTypes = lambda: types
        self.tableWidget.setRowCount(0)

        self.show()

    def hats_conversion(self):

        hats_file = QtWidgets.QFileDialog.getOpenFileName(self, "Select HATS File", "", 'txt (*.txt)')[0]

        if hats_file == '':
            no_file_selected()
        else:

            hats_data = pd.read_csv(hats_file, sep="\t", skiprows=3, header=None, on_bad_lines='skip')

            txt_name = []

            for i in range(1, 148, 2):
                txt_name.append(hats_data.loc[0, i])

            hats_data = hats_data.drop([0, 1])
            hats_data = hats_data.reset_index(drop=True)
            # Select folder to save data output
            save_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select HATS Save Folder")
            # iteration variable for lists in following for loop
            i = 1
            # iterate over all text names, allocate corresponding data, and then save as txt
            for j in range(0, len(txt_name)):
                test_df_1 = hats_data[0].values.tolist()
                test_df_2 = hats_data[i].values.tolist()
                test_df_3 = hats_data[i + 1].values.tolist()

                export_df = pd.DataFrame(
                    {'0': test_df_1,
                     '1': test_df_2,
                     '2': test_df_3
                     })

                save_file = save_folder + '/' + txt_name[j] + '.txt'
                export_df.to_csv(save_file, sep='\t', index=False, na_rep='NaN', header=False)
                i = i + 2

            process_completed()

    def sams_conversion(self):

        sams_file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select SAMS Folder")

        if sams_file == '':
            no_file_selected()
        else:
            output_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select/Create Save Folder")

            if output_folder == '':
                no_file_selected()

            else:

                file_names = []
                for x in os.listdir(sams_file):
                    if x.endswith(".txt"):
                        file_names.append(x)

                for i in range(len(file_names)):
                    newPath = shutil.copy(os.path.join(sams_file, file_names[i]), output_folder)

                    sams_data = pd.read_csv(newPath, sep="\t", skiprows=5, header=None, on_bad_lines='skip')

                    sams_data.to_csv(newPath, sep='\t', index=False, na_rep='NaN', header=False)

                process_completed()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Drop and event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())
            return True
        return super().eventFilter(source, event)

    def addFile(self, filepath):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item = QtWidgets.QTableWidgetItem(filepath)
        self.tableWidget.setItem(row, 0, item)
        self.tableWidget.resizeColumnToContents(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("D:/Python Projects/HATS SAMS Conversion/Icon/Vituix_Converter_Icon_R1.ico"))
    win = MyMainWindow()
    sys.exit(app.exec_())
