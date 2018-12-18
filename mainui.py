# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

# Qt Creator自动生成的（见上面的英文），所以不要问为什么没有注释(✺ω✺)

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.topframe = QtWidgets.QFrame(self.centralwidget)
        self.topframe.setGeometry(QtCore.QRect(0, 0, 1280, 120))
        self.topframe.setStyleSheet("background-color: rgb(191, 45, 45);")
        self.topframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topframe.setObjectName("topframe")
        self.title = QtWidgets.QLabel(self.topframe)
        self.title.setGeometry(QtCore.QRect(25, 25, 331, 71))
        self.title.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: Bold 75 24pt \"Microsoft YaHei UI\";\n"
"")
        self.title.setObjectName("title")
        self.sideframe = QtWidgets.QFrame(self.centralwidget)
        self.sideframe.setGeometry(QtCore.QRect(0, 120, 200, 600))
        self.sideframe.setStyleSheet("background-color: rgb(245, 245, 247);")
        self.sideframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sideframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sideframe.setObjectName("sideframe")
        self.label = QtWidgets.QLabel(self.sideframe)
        self.label.setGeometry(QtCore.QRect(30, 40, 181, 41))
        self.label.setStyleSheet("color: rgb(136, 136, 136);\n"
"font: 75 15pt \"Microsoft YaHei UI\";")
        self.label.setObjectName("label")
        self.videoinput = QtWidgets.QPushButton(self.sideframe)
        self.videoinput.setGeometry(QtCore.QRect(20, 350, 160, 60))
        self.videoinput.setToolTip("")
        self.videoinput.setAutoFillBackground(False)
        self.videoinput.setStyleSheet("QPushButton{\n"
"    font: 30pt \"Microsoft YaHei UI\";\n"
"                   background-color:rgb(245, 245, 247);                  \n"
"                   border-radius:10px;                 \n"
"                   border-color:rgba(255,255,255,30);    \n"
"                   font:bold 20px;                       \n"
"                   color:rgb(119, 119, 119);                \n"
"                                          \n"
"                   }\n"
"\n"
"\n"
"QPushButton:hover{\n"
"                   background-color:rgb(209, 209, 211);\n"
"                   border-color:rgba(255,255,255,30);\n"
"                   border-style:inset;\n"
"                   color:rgb(0, 0, 0);\n"
"                   }\n"
"\n"
"\n"
"\n"
"                   \n"
"               ")
        self.videoinput.setObjectName("videoinput")
        self.photoinput = QtWidgets.QPushButton(self.sideframe)
        self.photoinput.setGeometry(QtCore.QRect(20, 160, 160, 60))
        self.photoinput.setToolTip("")
        self.photoinput.setAutoFillBackground(False)
        self.photoinput.setStyleSheet("QPushButton{\n"
"    font: 30pt \"Microsoft YaHei UI\";\n"
"                   background-color:rgb(209, 209, 211);                  \n"
"                   border-radius:10px;                 \n"
"                   border-color:rgba(255,255,255,30);    \n"
"                   font:bold 20px;                       \n"
"                   color:rgb(0, 0, 0);                \n"
"                                          \n"
"                   }")
        self.photoinput.setObjectName("photoinput")
        self.generate_v = QtWidgets.QPushButton(self.centralwidget)
        self.generate_v.setGeometry(QtCore.QRect(640, 640, 131, 41))
        self.generate_v.setStyleSheet("QPushButton{\n"
"    font: 30pt \"Microsoft YaHei UI\";\n"
"                   background-color:rgb(209, 209, 211);                  \n"
"                   border-radius:10px;                 \n"
"                   border-color:rgba(255,255,255,30);    \n"
"                   font:bold 20px;                       \n"
"                   color:rgb(0, 0, 0);                \n"
"                                          \n"
"                   }")
        self.generate_v.setObjectName("generate_v")
        self.generate_p = QtWidgets.QPushButton(self.centralwidget)
        self.generate_p.setGeometry(QtCore.QRect(640, 640, 131, 41))
        self.generate_p.setStyleSheet("QPushButton{\n"
"    font: 30pt \"Microsoft YaHei UI\";\n"
"                   background-color:rgb(209, 209, 211);                  \n"
"                   border-radius:10px;                 \n"
"                   border-color:rgba(255,255,255,30);    \n"
"                   font:bold 20px;                       \n"
"                   color:rgb(0, 0, 0);                \n"
"                                          \n"
"                   }")
        self.generate_p.setObjectName("generate_p")
        self.findfile = QtWidgets.QFrame(self.centralwidget)
        self.findfile.setGeometry(QtCore.QRect(450, 160, 541, 61))
        self.findfile.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.findfile.setFrameShadow(QtWidgets.QFrame.Raised)
        self.findfile.setObjectName("findfile")
        self.textEdit = QtWidgets.QTextEdit(self.findfile)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 431, 51))
        self.textEdit.setObjectName("textEdit")
        self.seekv = QtWidgets.QPushButton(self.findfile)
        self.seekv.setGeometry(QtCore.QRect(440, 10, 93, 30))
        self.seekv.setStyleSheet("background-color: rgb(242, 242, 242);\n"
"border-radius:8px;   ")
        self.seekv.setObjectName("seekv")
        self.seekp = QtWidgets.QPushButton(self.findfile)
        self.seekp.setGeometry(QtCore.QRect(440, 10, 93, 30))
        self.seekp.setStyleSheet("background-color: rgb(242, 242, 242);\n"
"border-radius:8px;   ")
        self.seekp.setObjectName("seekp")
        self.picture = QtWidgets.QFrame(self.centralwidget)
        self.picture.setGeometry(QtCore.QRect(370, 220, 671, 411))
        self.picture.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.picture.setFrameShadow(QtWidgets.QFrame.Raised)
        self.picture.setObjectName("picture")
        self.picture_v = QtWidgets.QFrame(self.picture)
        self.picture_v.setGeometry(QtCore.QRect(0, 10, 671, 391))
        self.picture_v.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.picture_v.setFrameShadow(QtWidgets.QFrame.Raised)
        self.picture_v.setObjectName("picture_v")
        self.picture_p = QtWidgets.QTableWidget(self.picture)
        self.picture_p.setGeometry(QtCore.QRect(5, 85, 660, 200))
        self.picture_p.setObjectName("picture_p")
        self.picture_p.setColumnCount(0)
        self.picture_p.setRowCount(0)
        self.imageshow = QtWidgets.QLabel(self.centralwidget)
        self.imageshow.setGeometry(QtCore.QRect(240, 130, 171, 141))
        self.imageshow.setText("")
        self.imageshow.setObjectName("imageshow")
        self.afterimageshow = QtWidgets.QLabel(self.centralwidget)
        self.afterimageshow.setGeometry(QtCore.QRect(1080, 140, 91, 91))
        self.afterimageshow.setText("")
        self.afterimageshow.setObjectName("afterimageshow")
        self.generate_v.raise_()
        self.topframe.raise_()
        self.sideframe.raise_()
        self.generate_p.raise_()
        self.findfile.raise_()
        self.picture.raise_()
        self.imageshow.raise_()
        self.afterimageshow.raise_()
        self.seekv.raise_()
        self.textEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.videoinput.clicked.connect(MainWindow.video_mode)
        self.photoinput.clicked.connect(MainWindow.image_mode)
        self.generate_v.clicked.connect(MainWindow.generate_view_of_videos)
        self.generate_p.clicked.connect(MainWindow.generate_view_of_images)
        self.seekp.clicked.connect(MainWindow.get_image)
        self.seekv.clicked.connect(MainWindow.get_video)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">人脸情绪识别</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">请选择输入模式</span></p></body></html>"))
        self.videoinput.setText(_translate("MainWindow", "视频输入"))
        self.photoinput.setText(_translate("MainWindow", "图片输入"))
        self.generate_v.setText(_translate("MainWindow", "生成曲线图"))
        self.generate_p.setText(_translate("MainWindow", "生成信息表"))
        self.seekv.setText(_translate("MainWindow", "浏览"))
        self.seekp.setText(_translate("MainWindow", "浏览"))

