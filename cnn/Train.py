# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Train.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import *
from cnn.CNNs import CNN
from cnn.Test import Test
from cnn.SheetTest import SheetTest
from cnn.LoadData import LoadData

class Train(object):
    def __init__(self):
        load_train = LoadData()
        self.folder_data_train = load_train.folder_data_train
        self.train_generator, self.x_train, self.y_train, self.x_vald, self.y_vald = load_train.loadDataTrain()
        self.input_shape = (load_train.img_rows, load_train.img_cols, 1)

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
        self.btn_testing_form = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_testing_form.setObjectName("btn_testing_form")
        self.gridLayout.addWidget(self.btn_testing_form, 8, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.txt_epochs = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txt_epochs.setObjectName("txt_epochs")
        self.txt_epochs.setText("10")
        self.gridLayout.addWidget(self.txt_epochs, 1, 1, 1, 1)
        self.btn_training = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_training.setObjectName("btn_training")
        self.gridLayout.addWidget(self.btn_training, 5, 4, 1, 1)
        self.txt_lr = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txt_lr.setObjectName("txt_lr")
        self.txt_lr.setText("0.001")
        self.gridLayout.addWidget(self.txt_lr, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 5)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 5)
        self.source_training = QtWidgets.QLabel(self.gridLayoutWidget)
        self.source_training.setObjectName("source_training")
        self.gridLayout.addWidget(self.source_training, 3, 1, 1, 4)
        self.btn_sheettest_form = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_sheettest_form.setObjectName("btn_sheettest_form")
        self.gridLayout.addWidget(self.btn_sheettest_form, 8, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 4)
        self.result_training = QtWidgets.QLabel(self.gridLayoutWidget)
        self.result_training.setObjectName("result_training")
        self.gridLayout.addWidget(self.result_training, 6, 0, 1, 4)
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

        validator_epoch = QIntValidator(0, 100, self.txt_epochs)
        self.txt_epochs.setValidator(validator_epoch)

        validator_lr = QDoubleValidator(0.0001, 0.9999, 4, self.txt_lr)
        self.txt_lr.setValidator(validator_lr)

        self.btn_training.clicked.connect(self.startTrain)
        self.btn_testing_form.clicked.connect(self.testingForm)
        self.btn_sheettest_form.clicked.connect(self.sheetTestForm)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Jumlah Epoch"))
        self.btn_training.setText(_translate("MainWindow", "Start Training"))
        self.btn_testing_form.setText(_translate("MainWindow", "Testing Form"))
        self.label_4.setText(_translate("MainWindow", "Training"))
        self.label_2.setText(_translate("MainWindow", "Learning Rate"))
        self.result_training.setText(_translate("MainWindow", ""))
        self.label_3.setText(_translate("MainWindow", "Setting"))
        self.label_5.setText(_translate("MainWindow", "Source :"))
        self.source_training.setText(_translate("MainWindow", self.folder_data_train))
        self.btn_sheettest_form.setText(_translate("MainWindow", "SheetTest Form"))

    def startTrain(self):
        if self.result_training.text() != "":
            self.result_training.setText("")

        if self.txt_lr.text() == "" or self.txt_epochs.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Maaf epoch atau learning rate kosong. Silahkan dilengkapi.")
            msg.setWindowTitle("Informasi")
            msg.exec_()
        else:
            epochs = self.txt_epochs.text()
            epochs = int(epochs)
            lr = self.txt_lr.text()
            lr = float(lr)
            batch_size = 128

            cnn = CNN(self.input_shape, len(self.train_generator.class_indices), lr)
            model = cnn.my_model()

            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(epochs)

            history = model.fit(self.x_train, self.y_train,
                                batch_size=batch_size,
                                epochs=epochs,
                                verbose=1,
                                validation_data=(self.x_vald, self.y_vald))

            self.progressBar.setValue(epochs)

            evaluation = model.evaluate(self.x_vald, self.y_vald, batch_size=batch_size, verbose=1)
            print('Kesimpulan dari training dataset memiliki loss : %.2f, accuracy : %.2f' % (
            evaluation[0], evaluation[1]))
            self.result_training.setText(
                'Kesimpulan dari training dataset memiliki loss : %.2f, accuracy : %.2f' % (
                evaluation[0], evaluation[1])
            )

            model.save('D:/Projects/Python/PycharmProjects/OMR/cnn/model.h5')

    def testingForm(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Test()
        self.ui.setupUi(self.window)
        self.window.show()

    def sheetTestForm(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = SheetTest()
        self.ui.setupUi(self.window)
        self.window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Train()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

