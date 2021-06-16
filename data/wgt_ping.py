# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets
from data.main_ping import *

    #Форма пинга

class PingForm(object):
    def setupUi(self, Form):
        Form.resize(461, 40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 40))
        Form.setMaximumSize(QtCore.QSize(16777215, 40))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)

        #Добавление объектов

        self.led = QtWidgets.QPushButton(self.groupBox)
        self.led.setMaximumSize(QtCore.QSize(10, 10))
        self.horizontalLayout_2.addWidget(self.led)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_ms = QtWidgets.QLabel(self.groupBox)
        self.horizontalLayout_2.addWidget(self.label_ms)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_byte = QtWidgets.QLabel(self.groupBox)
        self.horizontalLayout_2.addWidget(self.label_byte)
        spacerItem2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_pkg = QtWidgets.QLabel(self.groupBox)
        self.horizontalLayout_2.addWidget(self.label_pkg)
        self.verticalLayout.addWidget(self.groupBox)
        
        #Имена обьектов

        Form.setObjectName("Form")
        self.led.setObjectName("led")
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label.setObjectName("label")
        self.label_ms.setObjectName("label_ms")
        self.label_byte.setObjectName("label_byte")
        self.label_pkg.setObjectName("label_pkg")

        QtCore.QMetaObject.connectSlotsByName(Form)

        self.retranslateUi(Form)



    def retranslateUi(self,Form):
        _translate = QtCore.QCoreApplication.translate
        # Form.setWindowTitle(_translate("Form", "Form"))
        # self.label.setText(_translate( "Form", "Kto ya"  ))
        # self.label_2.setText(_translate("Form", "20 ms"))
        # self.label_3.setText(_translate("Form", "32"))
        # self.label_pkg.setText(_translate("Form", "0"))