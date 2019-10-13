# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SheetTest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2 as cv
from PyQt5.QtWidgets import *
from keras.models import load_model
from cnn.LoadData import LoadData
import pandas as pd

class SheetTest(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 381))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.btnSelectImage = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnSelectImage.setObjectName("btnSelectImage")
        self.gridLayout.addWidget(self.btnSelectImage, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.btnPredict = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnPredict.setObjectName("btnPredict")
        self.gridLayout.addWidget(self.btnPredict, 2, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(450, 160))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 2, 1, 1)
        self.viewImage = QtWidgets.QLabel(self.gridLayoutWidget)
        self.viewImage.setMinimumSize(QtCore.QSize(450, 160))
        self.viewImage.setFrameShape(QtWidgets.QFrame.Box)
        self.viewImage.setText("")
        self.viewImage.setObjectName("viewImage")
        self.gridLayout.addWidget(self.viewImage, 0, 2, 1, 1)
        self.resultTest = QtWidgets.QLabel(self.gridLayoutWidget)
        self.resultTest.setObjectName("resultTest")
        self.gridLayout.addWidget(self.resultTest, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btnSelectImage.clicked.connect(self.loadImage)
        self.btnPredict.clicked.connect(self.startPredict)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnSelectImage.setText(_translate("MainWindow", "Select Image"))
        self.btnPredict.setText(_translate("MainWindow", "Predict"))
        self.resultTest.setText(_translate("MainWindow", ""))

    def loadImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "",
                                                            "Image Filed (*.png)")
        if fileName:
            pixmap = QtGui.QPixmap(fileName)
            pixmap = pixmap.scaled(self.viewImage.width(), self.viewImage.height(), QtCore.Qt.KeepAspectRatio)
            self.viewImage.setPixmap(pixmap)
            self.viewImage.setAlignment(QtCore.Qt.AlignCenter)

            self.prePredict(fileName)

    def prePredict(self, fileName):
        src = cv.imread(fileName, cv.IMREAD_COLOR)
        # grayscale
        if len(src.shape) != 2:
            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        else:
            gray = src

        # invert color
        gray = cv.bitwise_not(gray)

        # threshold
        bw = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)[1]

        # REMOVE STAFF LINE
        # init
        # Create the images that will use to extract the horizontal and vertical lines
        horizontal = np.copy(bw)
        vertical = np.copy(bw)
        # horiz
        # Specify size on horizontal axis
        cols = horizontal.shape[1]
        horizontal_size = cols / 30
        # vert
        # Specify size on vertical axis
        rows = vertical.shape[0]
        verticalsize = 4
        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
        # Apply morphology operations
        vertical = cv.erode(vertical, verticalStructure)
        vertical = cv.dilate(vertical, verticalStructure)

        img = vertical

        _, contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        print('no of shapes {0}'.format(len(contours)))

        for i in range(len(contours)):
            idx = i  # The index of the contour that surrounds your object
            mask = np.zeros_like(img)  # Create mask where white is what we want, black otherwise
            cv.drawContours(mask, contours, idx, 255, -1)  # Draw filled contour in mask
            out = np.zeros_like(img)  # Extract out the object and place into output image
            out = gray

            # Now crop
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            w = (bottomx-topx) % 30
            h = (bottomy-topy) % 50
            if topx<30:
                out = out[topx:bottomx+30+w, topy-60:bottomy+30+h]
            elif topy<50:
                out = out[topx-60:bottomx+30+w, topy:bottomy+30+h]
            elif topx<30 and topy<50:
                out = out[topx:bottomx+30+w, topy:bottomy+30+h]
            else:
                out = out[topx-30:bottomx+30+w, topy-30:bottomy+30+h]

            out = cv.bitwise_not(out)

            out = cv.resize(out, (30, 50))

            cv.imwrite("D:/Projects/Python/PycharmProjects/OMR/cnn/data_testing_sheet/test_folder/%d.png" % (i), out)

    def addRow(self, row, itemLabels=[]):
        for i in range(0, 3):
            item = QTableWidgetItem()
            item.setText(itemLabels[i])
            self.tableWidget.setItem(row, i, item)

    def startPredict(self):
        load_data = LoadData()
        self.folder_data_test_sheet = load_data.folder_data_test_sheet
        self.train_generator, self.x_train, self.y_train, self.x_vald, self.y_vald = load_data.loadDataTrain()
        self.test_generator, self.x_test = load_data.loadDataTest(self.folder_data_test_sheet)

        model = load_model('D:/Projects/Python/PycharmProjects/OMR/cnn/model.h5')

        self.test_generator.reset()
        pred = model.predict_generator(self.test_generator, verbose=1)

        predicted_class_indices = np.argmax(pred, axis=1)

        labels = (self.train_generator.class_indices)
        labels = dict((v, k) for k, v in labels.items())
        predictions = [labels[k] for k in predicted_class_indices]
        path = self.test_generator.filenames

        filenames = []
        for x in range(len(path)):
            filenames.append(path[x][12:len(path[x]) - 8])

        true_pred = 0
        compare = []
        for x in range(len(filenames)):
            if filenames[x] == predictions[x]:
                true_pred = true_pred + 1
                compare.append("True")
            else:
                compare.append("False")

        row = len(self.test_generator)

        list_prediksi = []
        for i in range(row):
            list_prediksi.append([filenames[i], predictions[i], compare[i]])

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(3)
        columnHeaders = ['Filename', 'Predictions', 'Compare']
        self.tableWidget.setHorizontalHeaderLabels(columnHeaders)
        for i in range(row):
            self.addRow(i, list_prediksi[i])

        hasil_akurasi = true_pred / len(filenames) * 100
        self.resultTest.setText('Hasil prediksi lembaran musik memiliki akurasi : %.0f%%' % (hasil_akurasi))

        results = pd.DataFrame({"Filename": path,
                                "Predictions": predictions})
        results.to_csv("D:/Projects/Python/PycharmProjects/OMR/cnn/Prediksi_sheet.csv", index=False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SheetTest()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

