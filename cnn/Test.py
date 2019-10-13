# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from PyQt5.QtWidgets import *
from keras.models import load_model
import pandas as pd
from cnn.LoadData import LoadData

class Test(object):
    def __init__(self):
        load_data = LoadData()
        self.folder_data_test = load_data.folder_data_test
        self.train_generator, self.x_train, self.y_train, self.x_vald, self.y_vald = load_data.loadDataTrain()
        self.test_generator, self.x_test = load_data.loadDataTest(self.folder_data_test)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 361))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_predict = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_predict.setObjectName("btn_predict")
        self.gridLayout.addWidget(self.btn_predict, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 4)
        self.source_testing = QtWidgets.QLabel(self.gridLayoutWidget)
        self.source_testing.setObjectName("source_testing")
        self.gridLayout.addWidget(self.source_testing, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.result_testing = QtWidgets.QLabel(self.gridLayoutWidget)
        self.result_testing.setObjectName("result_testing")
        self.gridLayout.addWidget(self.result_testing, 2, 0, 1, 4)
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

        self.btn_predict.clicked.connect(self.startPredict)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_predict.setText(_translate("MainWindow", "Predict"))
        self.label.setText(_translate("MainWindow", "Source : "))
        self.source_testing.setText(_translate("MainWindow", self.folder_data_test))
        self.result_testing.setText(_translate("MainWindow", ""))

    def addRow(self, row, itemLabels=[]):
        for i in range(0, 3):
            item = QTableWidgetItem()
            item.setText(itemLabels[i])
            self.tableWidget.setItem(row, i, item)

    def startPredict(self):
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
            self.addRow(i,list_prediksi[i])

        hasil_akurasi = true_pred / len(filenames) * 100
        self.result_testing.setText('Hasil prediksi data baru memiliki akurasi : %.0f%%' % (hasil_akurasi))

        results = pd.DataFrame({"Filename": path,
                                "Predictions": predictions})
        results.to_csv("D:/Projects/Python/PycharmProjects/OMR/cnn/Prediksi.csv", index=False)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Test()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

