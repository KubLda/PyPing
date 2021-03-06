# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets
from data.wgt_init import MyWidget
from data.wgt_ping import PingForm
from data.execut import monitor
from threading import Thread
import sys, locale, subprocess, platform, time, os

    #Переменные

WidCount = []
layout_num = 0
layout = [0]
lost = [0]
tidentlst = 0
actv = 0
with open('data/cache/config_cache.ini', 'r') as file:
    lst = file.readlines()
del lst[0]
lst = [[str(n) for n in x.split()] for x in lst]

    #Описание основного окна

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(500, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(380, 400))
        qss_file = open('data/style/style_file.css').read()
        MainWindow.setStyleSheet(qss_file)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setSpacing(0)
        self.LabelBox = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LabelBox.sizePolicy().hasHeightForWidth())
        self.LabelBox.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.LabelBox)
        self.horizontalLayout.setContentsMargins(10, 0, -1, 0)
        self.LabelStatus = QtWidgets.QLabel(self.LabelBox)
        self.horizontalLayout.addWidget(self.LabelStatus)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.LabelIP = QtWidgets.QLabel(self.LabelBox)
        self.horizontalLayout.addWidget(self.LabelIP)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.LabelBox)
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addItem(spacerItem)
        self.LabelTime = QtWidgets.QLabel(self.LabelBox)
        self.horizontalLayout.addWidget(self.LabelTime)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.LabelBox)
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.LabelBox)
        self.TableIP = QtWidgets.QScrollArea(self.groupBox)
        self.TableIP.setWidgetResizable(True)
        self.TableIP.setObjectName("TableIP")
        self.verticalLayout_2.addWidget(self.TableIP)
        self.TableIPLayout  = QtWidgets.QVBoxLayout(self.TableIP)
        self.TableIPLayout.setObjectName("TableIPLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        def addSpacer():
            try:
                del self.TableIPLayout.spacerItem
                print('Удалил')
            except:
                self.TableIPLayout.addItem(spacerItem)
                print('Добавил')

        #Добавление виджетов

        tident = sum(1 for line in open("data/cache/config_cache.ini"))
        def addWidget(tident :int):
            ident = 0
            global WidCount
            global lst
            global lst_new
            global lost
            global layout_num
            global layout
            global tidentlst
            global actv
            layout_num += 1
            layout.append(layout_num)
            def rm_owgt():
                ident = 0
                global lst
                global tidentlst
                while ident <= tidentlst:
                    try:
                        self.NameWidget = lst[ident][0]
                        self.NameWidget.hide()
                        ident += 1
                    except:
                        break
            if actv == 1:
                rm_owgt()
                lst = lst_new
                WidCount = []
                lost = []
                ident = 0
            if tident > 0:
                try:
                    while ident <= tident:
                        self.NameWid = str(lst[ident][0])
                        lst[ident][0] = MyWidget()
                        self.NameWidget = lst[ident][0]
                        self.TableIPLayout.addWidget(self.NameWidget)
                        WidCount.append(self.NameWidget)
                        lost.append(0)
                        widget_style = open('data/style/wgt_file.css').read()
                        self.NameWidget.setStyleSheet(widget_style)
                        self.NameWidget.label.setText(self.NameWid)
                        self.NameWidget.setWindowModified(True)
                        self.NameWidget.label_ms.setText("0 ms")
                        ident += 1
                except:
                    None
            actv = 0
            tidentlst = tident
            addSpacer()
        try:
            addWidget(tident)
        except:
            print('Кончились хосты')

        
            #Обращение к функциям execute

        def func():
            global WidCount
            global lst  
            global lost
            tident = sum(1 for line in open("data/cache/config_cache.ini"))
            wid_on = open('data/style/wgt_on.css').read()
            wid_off = open('data/style/wgt_off.css').read()
            while True:
                try:
                    while ident < tident:
                        try: 
                            host = lst[ident][1]
                            output = monitor(host)
                            xmit_stats = output[0].split(",")
                            timing_stats = output[1].split("=")[1].split("/")
                            packet_loss = (xmit_stats[2].split("%")[0])
                            ping_avg = float(timing_stats[1])
                            self.NameWidget = WidCount[ident]
                            self.NameWidget.led.setStyleSheet(wid_on)
                            self.NameWidget.label_ms.setText(str(ping_avg) + " ms")
                            self.NameWidget.label_byte.setText("64")
                            self.NameWidget.label_pkg.setText(str(lost[ident]))
                        except:
                            lost[ident] += 1
                            self.NameWidget = WidCount[ident]
                            self.NameWidget.led.setStyleSheet(wid_off)
                            self.NameWidget.label_pkg.setText(str(lost[ident]))
                            self.NameWidget.label_byte.setText("64")
                            self.NameWidget.label_ms.setText("0 ms")

                        time.sleep(0.5)
                        ident += 1
                except:
                    ident = 0

        #Вызов функции пинга 

        thread2 = Thread(target=func)
        thread2.start()


        #Меню-бар
        
        def new_file(self):
            global tident
            global lst_new
            global actv
            fname = QtWidgets.QFileDialog.getOpenFileName()[0]
            try:
                f = open(fname, 'r')
                with f as file:
                    lst_new = file.readlines()
                del lst_new[0]
                lst_new = [[str(n) for n in x.split()] for x in lst_new]
                actv = 1
                tident = sum(1 for line in open(fname, 'r'))
                f = open(fname, 'r')
                with f as file:
                    text = file.readlines()
                    cache = open("data/cache/config_cache.ini", 'w')
                    cache.writelines(text)
                addWidget(tident)
            except:
                print('Не выбран файл')
        def open_file(self):
            print('OpenFile')
        def save_file(self):
            print('SaveFile')
        def save_as(self):
            print('SaveAs')
        def exit_app(self):
            print('Exit')
        self.verticalLayout.addWidget(self.groupBox)
        self.TableIPLayout.addItem(spacerItem)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 24))
        self.FileMenu = QtWidgets.QMenu(self.menubar)
        self.Settings = QtWidgets.QMenu(self.menubar)
        self.Help = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.NewFile = QtWidgets.QAction(MainWindow)
        self.OpenFile = QtWidgets.QAction(MainWindow)
        self.SaveFile = QtWidgets.QAction(MainWindow)
        self.SaveAs = QtWidgets.QAction(MainWindow)
        self.Exit = QtWidgets.QAction(MainWindow)
        self.AddIP = QtWidgets.QAction(MainWindow)
        self.DelIP = QtWidgets.QAction(MainWindow)
        self.Settings_2 = QtWidgets.QAction(MainWindow)
        self.About = QtWidgets.QAction(MainWindow)
        
        self.NewFile.triggered.connect(new_file)
        self.OpenFile.triggered.connect(open_file)
        self.SaveFile.triggered.connect(save_file)
        self.SaveAs.triggered.connect(save_as)
        self.Exit.triggered.connect(exit_app)


        self.FileMenu.addAction(self.NewFile)
        self.FileMenu.addAction(self.OpenFile)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SaveFile)
        self.FileMenu.addAction(self.SaveAs)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.Exit)
        self.Settings.addAction(self.AddIP)
        self.Settings.addAction(self.DelIP)
        self.Settings.addSeparator()
        self.Settings.addAction(self.Settings_2)
        self.Help.addAction(self.About)
        self.menubar.addAction(self.FileMenu.menuAction())
        self.menubar.addAction(self.Settings.menuAction())
        self.menubar.addAction(self.Help.menuAction())

        

        #Имена обьектов

        MainWindow.setObjectName("MainWindow")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LabelBox.setObjectName("LabelBox")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LabelStatus.setObjectName("LabelStatus")
        self.LabelIP.setObjectName("LabelIP")
        self.label.setObjectName("label")
        self.LabelTime.setObjectName("LabelTime")
        self.label_2.setObjectName("label_2")
        self.FileMenu.setObjectName("FileMenu")
        self.menubar.setObjectName("menubar")
        self.TableIPLayout.setObjectName("TableIPLayout")
        self.TableIP.setObjectName("TableIP")
        self.Settings.setObjectName("Settings")
        self.Help.setObjectName("Help")
        self.NewFile.setObjectName("NewFile")
        self.OpenFile.setObjectName("OpenFile")
        self.SaveFile.setObjectName("SaveFile")
        self.SaveAs.setObjectName("SaveAs")
        self.Exit.setObjectName("Exit")
        self.AddIP.setObjectName("AddIP")
        self.DelIP.setObjectName("DelIP")
        self.Settings_2.setObjectName("Settings_2")
        self.About.setObjectName("About")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.NewFile.clicked.connect()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyPing"))
        self.LabelStatus.setText(_translate("MainWindow", "Статус:"))
        self.LabelIP.setText(_translate("MainWindow", "Имя хоста:"))
        self.label.setText(_translate("MainWindow", "Время:"))
        self.LabelTime.setText(_translate("MainWindow", "Размер \n""пакета:"))
        self.label_2.setText(_translate("MainWindow", "Пропущенные\n""пакеты:"))
        self.FileMenu.setTitle(_translate("MainWindow", "Файл"))
        self.Settings.setTitle(_translate("MainWindow", "Действие"))
        self.Help.setTitle(_translate("MainWindow", "Справка"))
        self.NewFile.setText(_translate("MainWindow", "Новый Файл"))
        self.OpenFile.setText(_translate("MainWindow", "Открыть Файл"))
        self.SaveFile.setText(_translate("MainWindow", "Сохранить"))
        self.SaveAs.setText(_translate("MainWindow", "Сохранить как"))
        self.Exit.setText(_translate("MainWindow", "Выход"))
        self.AddIP.setText(_translate("MainWindow", "Показать Ping всех каналов"))
        self.DelIP.setText(_translate("MainWindow", "Показать Tracert всех каналов"))
        self.Settings_2.setText(_translate("MainWindow", "Настройки"))
        self.About.setText(_translate("MainWindow", "О программе"))