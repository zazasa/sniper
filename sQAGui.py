# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sQAGui.ui'
#
# Created: Mon Nov 25 18:21:05 2013
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.chanBox = QtGui.QGroupBox(self.centralwidget)
        self.chanBox.setGeometry(QtCore.QRect(47, 9, 161, 461))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chanBox.sizePolicy().hasHeightForWidth())
        self.chanBox.setSizePolicy(sizePolicy)
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
        self.gridLayout_3.setHorizontalSpacing(5)
        self.gridLayout_3.setVerticalSpacing(20)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ch1 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch1.sizePolicy().hasHeightForWidth())
        self.ch1.setSizePolicy(sizePolicy)
        self.ch1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.gridLayout_3.addWidget(self.ch1, 1, 0, 1, 1)
        self.ch2 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch2.sizePolicy().hasHeightForWidth())
        self.ch2.setSizePolicy(sizePolicy)
        self.ch2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.gridLayout_3.addWidget(self.ch2, 2, 0, 1, 1)
        self.ch11 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch11.sizePolicy().hasHeightForWidth())
        self.ch11.setSizePolicy(sizePolicy)
        self.ch11.setObjectName(_fromUtf8("ch11"))
        self.gridLayout_3.addWidget(self.ch11, 3, 1, 1, 1)
        self.ch10 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch10.sizePolicy().hasHeightForWidth())
        self.ch10.setSizePolicy(sizePolicy)
        self.ch10.setObjectName(_fromUtf8("ch10"))
        self.gridLayout_3.addWidget(self.ch10, 2, 1, 1, 1)
        self.ch7 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch7.sizePolicy().hasHeightForWidth())
        self.ch7.setSizePolicy(sizePolicy)
        self.ch7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch7.setObjectName(_fromUtf8("ch7"))
        self.gridLayout_3.addWidget(self.ch7, 7, 0, 1, 1)
        self.ch0 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch0.sizePolicy().hasHeightForWidth())
        self.ch0.setSizePolicy(sizePolicy)
        self.ch0.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch0.setObjectName(_fromUtf8("ch0"))
        self.gridLayout_3.addWidget(self.ch0, 0, 0, 1, 1)
        self.ch4 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch4.sizePolicy().hasHeightForWidth())
        self.ch4.setSizePolicy(sizePolicy)
        self.ch4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch4.setObjectName(_fromUtf8("ch4"))
        self.gridLayout_3.addWidget(self.ch4, 4, 0, 1, 1)
        self.ch8 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch8.sizePolicy().hasHeightForWidth())
        self.ch8.setSizePolicy(sizePolicy)
        self.ch8.setObjectName(_fromUtf8("ch8"))
        self.gridLayout_3.addWidget(self.ch8, 0, 1, 1, 1)
        self.ch3 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch3.sizePolicy().hasHeightForWidth())
        self.ch3.setSizePolicy(sizePolicy)
        self.ch3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.gridLayout_3.addWidget(self.ch3, 3, 0, 1, 1)
        self.ch5 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch5.sizePolicy().hasHeightForWidth())
        self.ch5.setSizePolicy(sizePolicy)
        self.ch5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch5.setObjectName(_fromUtf8("ch5"))
        self.gridLayout_3.addWidget(self.ch5, 5, 0, 1, 1)
        self.ch14 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch14.sizePolicy().hasHeightForWidth())
        self.ch14.setSizePolicy(sizePolicy)
        self.ch14.setObjectName(_fromUtf8("ch14"))
        self.gridLayout_3.addWidget(self.ch14, 6, 1, 1, 1)
        self.ch12 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch12.sizePolicy().hasHeightForWidth())
        self.ch12.setSizePolicy(sizePolicy)
        self.ch12.setObjectName(_fromUtf8("ch12"))
        self.gridLayout_3.addWidget(self.ch12, 4, 1, 1, 1)
        self.ch6 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch6.sizePolicy().hasHeightForWidth())
        self.ch6.setSizePolicy(sizePolicy)
        self.ch6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ch6.setObjectName(_fromUtf8("ch6"))
        self.gridLayout_3.addWidget(self.ch6, 6, 0, 1, 1)
        self.ch13 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch13.sizePolicy().hasHeightForWidth())
        self.ch13.setSizePolicy(sizePolicy)
        self.ch13.setObjectName(_fromUtf8("ch13"))
        self.gridLayout_3.addWidget(self.ch13, 5, 1, 1, 1)
        self.ch9 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch9.sizePolicy().hasHeightForWidth())
        self.ch9.setSizePolicy(sizePolicy)
        self.ch9.setObjectName(_fromUtf8("ch9"))
        self.gridLayout_3.addWidget(self.ch9, 1, 1, 1, 1)
        self.ch15 = QtGui.QCheckBox(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ch15.sizePolicy().hasHeightForWidth())
        self.ch15.setSizePolicy(sizePolicy)
        self.ch15.setObjectName(_fromUtf8("ch15"))
        self.gridLayout_3.addWidget(self.ch15, 7, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_6)
        spacerItem = QtGui.QSpacerItem(20, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.allONButton = QtGui.QPushButton(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allONButton.sizePolicy().hasHeightForWidth())
        self.allONButton.setSizePolicy(sizePolicy)
        self.allONButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.allONButton.setObjectName(_fromUtf8("allONButton"))
        self.horizontalLayout_12.addWidget(self.allONButton)
        self.allOFFButton = QtGui.QPushButton(self.chanBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allOFFButton.sizePolicy().hasHeightForWidth())
        self.allOFFButton.setSizePolicy(sizePolicy)
        self.allOFFButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.allOFFButton.setObjectName(_fromUtf8("allOFFButton"))
        self.horizontalLayout_12.addWidget(self.allOFFButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 9, 42, 88))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.loadButton = QtGui.QToolButton(self.layoutWidget)
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
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(220, 10, 411, 243))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
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
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.drawButton = QtGui.QPushButton(self.groupBox)
        self.drawButton.setMinimumSize(QtCore.QSize(140, 40))
        self.drawButton.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.drawButton.setFont(font)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-refresh"))
        self.drawButton.setIcon(icon)
        self.drawButton.setObjectName(_fromUtf8("drawButton"))
        self.horizontalLayout_3.addWidget(self.drawButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 92, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem4)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.prevButton = QtGui.QPushButton(self.groupBox)
        self.prevButton.setObjectName(_fromUtf8("prevButton"))
        self.horizontalLayout_11.addWidget(self.prevButton)
        self.nextButton = QtGui.QPushButton(self.groupBox)
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.horizontalLayout_11.addWidget(self.nextButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem5)
        self.allButton = QtGui.QPushButton(self.groupBox)
        self.allButton.setObjectName(_fromUtf8("allButton"))
        self.horizontalLayout_11.addWidget(self.allButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.bgButton = QtGui.QPushButton(self.groupBox)
        self.bgButton.setObjectName(_fromUtf8("bgButton"))
        self.horizontalLayout_13.addWidget(self.bgButton)
        self.sbgButton = QtGui.QPushButton(self.groupBox)
        self.sbgButton.setObjectName(_fromUtf8("sbgButton"))
        self.horizontalLayout_13.addWidget(self.sbgButton)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_15.addWidget(self.label_11)
        self.numBinBox_3 = QtGui.QSpinBox(self.groupBox)
        self.numBinBox_3.setMaximum(99999)
        self.numBinBox_3.setSingleStep(5)
        self.numBinBox_3.setProperty("value", 10)
        self.numBinBox_3.setObjectName(_fromUtf8("numBinBox_3"))
        self.horizontalLayout_15.addWidget(self.numBinBox_3)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_15)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem6)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setGeometry(QtCore.QRect(220, 270, 411, 201))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
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
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.source = QtGui.QLineEdit(self.groupBox_2)
        self.source.setObjectName(_fromUtf8("source"))
        self.horizontalLayout_4.addWidget(self.source)
        self.horizontalLayout_19.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_16.addWidget(self.label_5)
        self.numBinBox = QtGui.QSpinBox(self.groupBox_2)
        self.numBinBox.setMaximum(99999)
        self.numBinBox.setSingleStep(50)
        self.numBinBox.setProperty("value", 100)
        self.numBinBox.setObjectName(_fromUtf8("numBinBox"))
        self.horizontalLayout_16.addWidget(self.numBinBox)
        self.horizontalLayout_19.addLayout(self.horizontalLayout_16)
        self.verticalLayout.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_10.addWidget(self.label_3)
        self.mFromBox = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mFromBox.sizePolicy().hasHeightForWidth())
        self.mFromBox.setSizePolicy(sizePolicy)
        self.mFromBox.setMinimumSize(QtCore.QSize(100, 0))
        self.mFromBox.setMaximum(999999999)
        self.mFromBox.setSingleStep(100)
        self.mFromBox.setObjectName(_fromUtf8("mFromBox"))
        self.horizontalLayout_10.addWidget(self.mFromBox)
        self.horizontalLayout_18.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_14.addWidget(self.label_4)
        self.mToBox = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mToBox.sizePolicy().hasHeightForWidth())
        self.mToBox.setSizePolicy(sizePolicy)
        self.mToBox.setMinimumSize(QtCore.QSize(100, 0))
        self.mToBox.setMaximum(999999999)
        self.mToBox.setSingleStep(100)
        self.mToBox.setObjectName(_fromUtf8("mToBox"))
        self.horizontalLayout_14.addWidget(self.mToBox)
        self.horizontalLayout_18.addLayout(self.horizontalLayout_14)
        self.verticalLayout.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_9.addWidget(self.label_10)
        self.sWidthBox = QtGui.QSpinBox(self.groupBox_2)
        self.sWidthBox.setMaximum(99999)
        self.sWidthBox.setSingleStep(1)
        self.sWidthBox.setProperty("value", 5)
        self.sWidthBox.setObjectName(_fromUtf8("sWidthBox"))
        self.horizontalLayout_9.addWidget(self.sWidthBox)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_7.addWidget(self.label_2)
        self.pSigmaBox = QtGui.QSpinBox(self.groupBox_2)
        self.pSigmaBox.setProperty("value", 1)
        self.pSigmaBox.setObjectName(_fromUtf8("pSigmaBox"))
        self.horizontalLayout_7.addWidget(self.pSigmaBox)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.fSigmaBox = QtGui.QSpinBox(self.groupBox_2)
        self.fSigmaBox.setProperty("value", 2)
        self.fSigmaBox.setObjectName(_fromUtf8("fSigmaBox"))
        self.horizontalLayout_5.addWidget(self.fSigmaBox)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_17)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.maxButton = QtGui.QPushButton(self.groupBox_2)
        self.maxButton.setObjectName(_fromUtf8("maxButton"))
        self.horizontalLayout.addWidget(self.maxButton)
        self.sumButton = QtGui.QPushButton(self.groupBox_2)
        self.sumButton.setObjectName(_fromUtf8("sumButton"))
        self.horizontalLayout.addWidget(self.sumButton)
        self.meanButton = QtGui.QPushButton(self.groupBox_2)
        self.meanButton.setObjectName(_fromUtf8("meanButton"))
        self.horizontalLayout.addWidget(self.meanButton)
        self.histButton = QtGui.QPushButton(self.groupBox_2)
        self.histButton.setObjectName(_fromUtf8("histButton"))
        self.horizontalLayout.addWidget(self.histButton)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.smoothButton = QtGui.QPushButton(self.groupBox_2)
        self.smoothButton.setObjectName(_fromUtf8("smoothButton"))
        self.horizontalLayout.addWidget(self.smoothButton)
        self.fitButton = QtGui.QPushButton(self.groupBox_2)
        self.fitButton.setObjectName(_fromUtf8("fitButton"))
        self.horizontalLayout.addWidget(self.fitButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
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
        self.loadButton.setToolTip(_translate("MainWindow", "Load File", None))
        self.loadButton.setText(_translate("MainWindow", "+", None))
        self.groupBox.setTitle(_translate("MainWindow", "Graph", None))
        self.label_7.setText(_translate("MainWindow", "Y:", None))
        self.yButton_1.setText(_translate("MainWindow", "yValue", None))
        self.label_8.setText(_translate("MainWindow", "X:", None))
        self.xButton_1.setText(_translate("MainWindow", "xValue", None))
        self.showMarkCB_1.setText(_translate("MainWindow", "Show Markers", None))
        self.showLineCB_1.setText(_translate("MainWindow", "Show Line", None))
        self.showLegendCB_1.setText(_translate("MainWindow", "Show Legend", None))
        self.drawButton.setToolTip(_translate("MainWindow", "Update", None))
        self.drawButton.setText(_translate("MainWindow", "Draw", None))
        self.prevButton.setText(_translate("MainWindow", "Prev", None))
        self.nextButton.setText(_translate("MainWindow", "Next", None))
        self.allButton.setText(_translate("MainWindow", "Persistence", None))
        self.bgButton.setText(_translate("MainWindow", "BackGround", None))
        self.sbgButton.setText(_translate("MainWindow", "Source - BG", None))
        self.label_11.setText(_translate("MainWindow", "bgIter:", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Measure", None))
        self.label.setText(_translate("MainWindow", "Source:", None))
        self.label_5.setText(_translate("MainWindow", "nBins:", None))
        self.label_3.setText(_translate("MainWindow", "from", None))
        self.label_4.setText(_translate("MainWindow", "To:", None))
        self.label_10.setText(_translate("MainWindow", "sWidth:", None))
        self.label_2.setText(_translate("MainWindow", "pSigma:", None))
        self.label_6.setText(_translate("MainWindow", "fSigma:", None))
        self.maxButton.setText(_translate("MainWindow", "Max", None))
        self.sumButton.setText(_translate("MainWindow", "Sum", None))
        self.meanButton.setText(_translate("MainWindow", "Mean", None))
        self.histButton.setText(_translate("MainWindow", "Hist", None))
        self.smoothButton.setText(_translate("MainWindow", "Smooth", None))
        self.fitButton.setText(_translate("MainWindow", "Fit", None))
