# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sGPlotGui.ui'
#
# Created: Sat Oct 19 17:20:16 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.loadButton = QtGui.QToolButton(self.centralwidget)
        self.loadButton.setMinimumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.loadButton.setFont(font)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.loadButton.setIcon(icon)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.verticalLayout_7.addWidget(self.loadButton)
        self.drawButton = QtGui.QToolButton(self.centralwidget)
        self.drawButton.setMinimumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.drawButton.setFont(font)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-refresh"))
        self.drawButton.setIcon(icon)
        self.drawButton.setObjectName(_fromUtf8("drawButton"))
        self.verticalLayout_7.addWidget(self.drawButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.chanBox = QtGui.QGroupBox(self.centralwidget)
        self.chanBox.setStyleSheet(_fromUtf8("QGroupBox  {\n"
"\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"    font-weight: bold\n"
"}\n"
" \n"
"QGroupBox::title  {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* position at the top center */\n"
"    padding: 0 3px;\n"
"}"))
        self.chanBox.setObjectName(_fromUtf8("chanBox"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.chanBox)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_3.setVerticalSpacing(20)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ch1 = QtGui.QCheckBox(self.chanBox)
        self.ch1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.gridLayout_3.addWidget(self.ch1, 1, 0, 1, 1)
        self.ch2 = QtGui.QCheckBox(self.chanBox)
        self.ch2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.gridLayout_3.addWidget(self.ch2, 2, 0, 1, 1)
        self.ch11 = QtGui.QCheckBox(self.chanBox)
        self.ch11.setObjectName(_fromUtf8("ch11"))
        self.gridLayout_3.addWidget(self.ch11, 3, 1, 1, 1)
        self.ch10 = QtGui.QCheckBox(self.chanBox)
        self.ch10.setObjectName(_fromUtf8("ch10"))
        self.gridLayout_3.addWidget(self.ch10, 2, 1, 1, 1)
        self.ch7 = QtGui.QCheckBox(self.chanBox)
        self.ch7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch7.setObjectName(_fromUtf8("ch7"))
        self.gridLayout_3.addWidget(self.ch7, 7, 0, 1, 1)
        self.ch0 = QtGui.QCheckBox(self.chanBox)
        self.ch0.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch0.setObjectName(_fromUtf8("ch0"))
        self.gridLayout_3.addWidget(self.ch0, 0, 0, 1, 1)
        self.ch4 = QtGui.QCheckBox(self.chanBox)
        self.ch4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch4.setObjectName(_fromUtf8("ch4"))
        self.gridLayout_3.addWidget(self.ch4, 4, 0, 1, 1)
        self.ch8 = QtGui.QCheckBox(self.chanBox)
        self.ch8.setObjectName(_fromUtf8("ch8"))
        self.gridLayout_3.addWidget(self.ch8, 0, 1, 1, 1)
        self.ch3 = QtGui.QCheckBox(self.chanBox)
        self.ch3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.gridLayout_3.addWidget(self.ch3, 3, 0, 1, 1)
        self.ch5 = QtGui.QCheckBox(self.chanBox)
        self.ch5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch5.setObjectName(_fromUtf8("ch5"))
        self.gridLayout_3.addWidget(self.ch5, 5, 0, 1, 1)
        self.ch14 = QtGui.QCheckBox(self.chanBox)
        self.ch14.setObjectName(_fromUtf8("ch14"))
        self.gridLayout_3.addWidget(self.ch14, 6, 1, 1, 1)
        self.ch12 = QtGui.QCheckBox(self.chanBox)
        self.ch12.setObjectName(_fromUtf8("ch12"))
        self.gridLayout_3.addWidget(self.ch12, 4, 1, 1, 1)
        self.ch6 = QtGui.QCheckBox(self.chanBox)
        self.ch6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch6.setObjectName(_fromUtf8("ch6"))
        self.gridLayout_3.addWidget(self.ch6, 6, 0, 1, 1)
        self.ch13 = QtGui.QCheckBox(self.chanBox)
        self.ch13.setObjectName(_fromUtf8("ch13"))
        self.gridLayout_3.addWidget(self.ch13, 5, 1, 1, 1)
        self.ch9 = QtGui.QCheckBox(self.chanBox)
        self.ch9.setObjectName(_fromUtf8("ch9"))
        self.gridLayout_3.addWidget(self.ch9, 1, 1, 1, 1)
        self.ch15 = QtGui.QCheckBox(self.chanBox)
        self.ch15.setObjectName(_fromUtf8("ch15"))
        self.gridLayout_3.addWidget(self.ch15, 7, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_6)
        spacerItem1 = QtGui.QSpacerItem(20, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.allONButton = QtGui.QPushButton(self.chanBox)
        self.allONButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.allONButton.setObjectName(_fromUtf8("allONButton"))
        self.horizontalLayout_12.addWidget(self.allONButton)
        self.allOFFButton = QtGui.QPushButton(self.chanBox)
        self.allOFFButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.allOFFButton.setObjectName(_fromUtf8("allOFFButton"))
        self.horizontalLayout_12.addWidget(self.allOFFButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_3.addWidget(self.chanBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet(_fromUtf8("QGroupBox  {\n"
"\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"    font-weight: bold\n"
"}\n"
" \n"
"QGroupBox::title  {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* position at the top center */\n"
"    padding: 0 3px;\n"
"}"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_8.addWidget(self.label_7)
        self.yButton_1 = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yButton_1.sizePolicy().hasHeightForWidth())
        self.yButton_1.setSizePolicy(sizePolicy)
        self.yButton_1.setMinimumSize(QtCore.QSize(150, 0))
        self.yButton_1.setObjectName(_fromUtf8("yButton_1"))
        self.horizontalLayout_8.addWidget(self.yButton_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_6.addWidget(self.label_8)
        self.xButton_1 = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xButton_1.sizePolicy().hasHeightForWidth())
        self.xButton_1.setSizePolicy(sizePolicy)
        self.xButton_1.setMinimumSize(QtCore.QSize(150, 0))
        self.xButton_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.xButton_1.setObjectName(_fromUtf8("xButton_1"))
        self.horizontalLayout_6.addWidget(self.xButton_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.showMarkCB_1 = QtGui.QCheckBox(self.groupBox)
        self.showMarkCB_1.setEnabled(True)
        self.showMarkCB_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showMarkCB_1.setChecked(True)
        self.showMarkCB_1.setObjectName(_fromUtf8("showMarkCB_1"))
        self.verticalLayout_3.addWidget(self.showMarkCB_1)
        self.showLineCB_1 = QtGui.QCheckBox(self.groupBox)
        self.showLineCB_1.setEnabled(True)
        self.showLineCB_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showLineCB_1.setObjectName(_fromUtf8("showLineCB_1"))
        self.verticalLayout_3.addWidget(self.showLineCB_1)
        self.showLegendCB_1 = QtGui.QCheckBox(self.groupBox)
        self.showLegendCB_1.setEnabled(True)
        self.showLegendCB_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showLegendCB_1.setChecked(False)
        self.showLegendCB_1.setObjectName(_fromUtf8("showLegendCB_1"))
        self.verticalLayout_3.addWidget(self.showLegendCB_1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.title1 = QtGui.QLineEdit(self.groupBox)
        self.title1.setObjectName(_fromUtf8("title1"))
        self.horizontalLayout_4.addWidget(self.title1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtGui.QSpacerItem(20, 92, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet(_fromUtf8("QGroupBox  {\n"
"\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"    font-weight: bold\n"
"}\n"
" \n"
"QGroupBox::title  {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* position at the top center */\n"
"    padding: 0 3px;\n"
"}"))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_9.addWidget(self.label_9)
        self.yButton_2 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yButton_2.sizePolicy().hasHeightForWidth())
        self.yButton_2.setSizePolicy(sizePolicy)
        self.yButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.yButton_2.setObjectName(_fromUtf8("yButton_2"))
        self.horizontalLayout_9.addWidget(self.yButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_7.addWidget(self.label_10)
        self.xButton_2 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xButton_2.sizePolicy().hasHeightForWidth())
        self.xButton_2.setSizePolicy(sizePolicy)
        self.xButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.xButton_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.xButton_2.setObjectName(_fromUtf8("xButton_2"))
        self.horizontalLayout_7.addWidget(self.xButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.showMarkCB_2 = QtGui.QCheckBox(self.groupBox_2)
        self.showMarkCB_2.setEnabled(True)
        self.showMarkCB_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showMarkCB_2.setChecked(True)
        self.showMarkCB_2.setObjectName(_fromUtf8("showMarkCB_2"))
        self.verticalLayout_5.addWidget(self.showMarkCB_2)
        self.showLineCB_2 = QtGui.QCheckBox(self.groupBox_2)
        self.showLineCB_2.setEnabled(True)
        self.showLineCB_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showLineCB_2.setObjectName(_fromUtf8("showLineCB_2"))
        self.verticalLayout_5.addWidget(self.showLineCB_2)
        self.showLegendCB_2 = QtGui.QCheckBox(self.groupBox_2)
        self.showLegendCB_2.setEnabled(True)
        self.showLegendCB_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showLegendCB_2.setChecked(False)
        self.showLegendCB_2.setObjectName(_fromUtf8("showLegendCB_2"))
        self.verticalLayout_5.addWidget(self.showLegendCB_2)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.title2 = QtGui.QLineEdit(self.groupBox_2)
        self.title2.setObjectName(_fromUtf8("title2"))
        self.horizontalLayout_5.addWidget(self.title2)
        self.verticalLayout_10.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtGui.QSpacerItem(20, 91, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.loadButton.setToolTip(_translate("MainWindow", "Load File", None))
        self.loadButton.setText(_translate("MainWindow", "+", None))
        self.drawButton.setToolTip(_translate("MainWindow", "Update", None))
        self.drawButton.setText(_translate("MainWindow", "R", None))
        self.chanBox.setTitle(_translate("MainWindow", "Channels", None))
        self.ch1.setText(_translate("MainWindow", "CH1", None))
        self.ch2.setText(_translate("MainWindow", "CH2", None))
        self.ch11.setText(_translate("MainWindow", "CH11", None))
        self.ch10.setText(_translate("MainWindow", "CH10", None))
        self.ch7.setText(_translate("MainWindow", "CH7", None))
        self.ch0.setText(_translate("MainWindow", "CH0", None))
        self.ch4.setText(_translate("MainWindow", "CH4", None))
        self.ch8.setText(_translate("MainWindow", "CH8", None))
        self.ch3.setText(_translate("MainWindow", "CH3", None))
        self.ch5.setText(_translate("MainWindow", "CH5", None))
        self.ch14.setText(_translate("MainWindow", "CH14", None))
        self.ch12.setText(_translate("MainWindow", "CH12", None))
        self.ch6.setText(_translate("MainWindow", "CH6", None))
        self.ch13.setText(_translate("MainWindow", "CH13", None))
        self.ch9.setText(_translate("MainWindow", "CH9", None))
        self.ch15.setText(_translate("MainWindow", "CH15", None))
        self.allONButton.setText(_translate("MainWindow", "ALL ON", None))
        self.allOFFButton.setText(_translate("MainWindow", "ALL OFF", None))
        self.groupBox.setTitle(_translate("MainWindow", "PAD1", None))
        self.label_7.setText(_translate("MainWindow", "Y:", None))
        self.yButton_1.setText(_translate("MainWindow", "yValue", None))
        self.label_8.setText(_translate("MainWindow", "X:", None))
        self.xButton_1.setText(_translate("MainWindow", "xValue", None))
        self.showMarkCB_1.setText(_translate("MainWindow", "Show Markers", None))
        self.showLineCB_1.setText(_translate("MainWindow", "Show Line", None))
        self.showLegendCB_1.setText(_translate("MainWindow", "Show Legend", None))
        self.label.setText(_translate("MainWindow", "Title:", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "PAD2", None))
        self.label_9.setText(_translate("MainWindow", "Y:", None))
        self.yButton_2.setText(_translate("MainWindow", "yValue", None))
        self.label_10.setText(_translate("MainWindow", "X:", None))
        self.xButton_2.setText(_translate("MainWindow", "xValue", None))
        self.showMarkCB_2.setText(_translate("MainWindow", "Show Markers", None))
        self.showLineCB_2.setText(_translate("MainWindow", "Show Line", None))
        self.showLegendCB_2.setText(_translate("MainWindow", "Show Legend", None))
        self.label_2.setText(_translate("MainWindow", "Title:", None))

