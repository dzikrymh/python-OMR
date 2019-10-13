import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from cnn.Train import Train

if __name__ == '__main__':
   a = QApplication(sys.argv)
   MainWindow = QtWidgets.QMainWindow()
   form = Train()
   form.setupUi(MainWindow)
   MainWindow.show()
   a.exec_()