# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controlboxwidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import client
import time
from datetime import datetime
import threading
import RPi.GPIO as GPIO


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        #self.openGLWidget = QtWidgets.QOpenGLWidget(Form)
        #self.openGLWidget.setGeometry(QtCore.QRect(320, 10, 640, 480))
        #self.openGLWidget.setObjectName("openGLWidget")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 121, 34))
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ConnectCrawler)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 60, 121, 34))
        self.pushButton_3.setStyleSheet("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.RecordVideos)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 140, 121, 34))
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.moveCrawler)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 10, 121, 34))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.TakePictures)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 220, 71, 41))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/up.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 290, 70, 40))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/down.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 240, 40, 70))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/right.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 240, 40, 70))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("images/left.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 460, 70, 70))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("images/letter-l.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(190, 460, 70, 70))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("images/letter-r.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(40, 430, 70, 40))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("images/up-arrow.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(40, 520, 70, 40))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("images/down-arrow.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(100, 460, 40, 70))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap("images/right-arrow.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(10, 460, 40, 70))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("images/left-arrow.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(190, 520, 70, 40))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("images/down-arrow.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(250, 460, 40, 70))
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap("images/right-arrow.png"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(160, 460, 40, 70))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("images/left-arrow.png"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(190, 430, 70, 40))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("images/up-arrow.png"))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(200, 340, 51, 51))
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap("images/R2.png"))
        self.label_15.setScaledContents(True)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(50, 340, 51, 51))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap("images/L2.png"))
        self.label_16.setScaledContents(True)
        self.label_16.setObjectName("label_16")
        self.spinBox = QtWidgets.QDoubleSpinBox(Form)
        self.spinBox.setGeometry(QtCore.QRect(180, 110, 61, 25))
        self.spinBox.setDecimals(1)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setObjectName("doubleSpinBox")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(180, 280, 131, 51))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.ShutdownCrawler)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(180, 240, 121, 34))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(180, 190, 121, 34))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.getDir)
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(50, 400, 51, 31))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("images/L1.png"))
        self.label_17.setScaledContents(True)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(200, 400, 51, 31))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("images/R1.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 60, 121, 34))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.pressed.connect(self.extendTether)
        self.pushButton_7.released.connect(self.stopTether)
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 110, 121, 34))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.pressed.connect(self.retractTether)
        self.pushButton_8.released.connect(self.stopTether)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(20, 160, 121, 34))
        #self.comboBox.setModelColumn(2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Tether off")
        self.comboBox.addItem("Forward")
        self.comboBox.addItem("Backward")
        self.label_19 = QtWidgets.QLabel(Form)
        self.label_19.setGeometry(QtCore.QRect(330, 500, 101, 31))
        self.label_19.setObjectName("label_19")
        self.label_19.setText("Distance")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(430, 500, 112, 34))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(self.resetTime)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)
        self.start = False
        self.count = 0
        self.dirpath = ""
        self.tetheron = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(33, GPIO.OUT)
        GPIO.setup(31, GPIO.OUT)
        GPIO.setwarnings(False)
        self.pwmtether = GPIO.PWM(33, 20000)

        #self.VBL = QVBoxLayout()

        self.FeedLabel = QtWidgets.QLabel(Form)
        self.FeedLabel.setGeometry(QtCore.QRect(320, 10, 640, 480))
        #self.VBL.addWidget(self.FeedLabel)

        #self.CancelBTN = QPushButton("Cancel")
        #self.CancelBTN.clicked.connect(self.CancelFeed)
        #self.VBL.addWidget(self.CancelBTN)

        

        #self.setLayout(self.VBL) interface="/dev/input/js0", connecting_using_ds4drv=False
        self.controller = client.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        self.takePicture = False
        self.recordVideo = False

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Connect"))
        self.pushButton_2.setText(_translate("Form", "Take picture"))
        self.pushButton_3.setText(_translate("Form", "Start recording"))
        self.pushButton_4.setText(_translate("Form", "Drive Forward"))
        self.pushButton_5.setText(_translate("Form", "Shutdown \n" "Crawler"))
        self.pushButton_6.setText(_translate("MainWindow", "Browse"))
        self.pushButton_7.setText(_translate("MainWindow", "Extend tether"))
        self.pushButton_8.setText(_translate("MainWindow", "Retarct tether"))
        self.pushButton_9.setText(_translate("MainWindow", "Reset"))
        
    def showTime(self):

        if self.start:
            self.count += 1

        if self.start:
            text = str(round(self.count / 60, 2)) + " ft"
            self.label_19.setText(text) 

    def resetTime(self):

        self.start = False
        self.count = 0
        self.label.setText("Distance") 

    def ConnectCrawler(self):
        controllerDisplay = ControllerDisplay(self.controller, self)
        self.thread = VideoThread(self.takePicture, self.dirpath)
        self.thread.start()
        self.thread.ImageUpdate.connect(self.ImageUpdateSlot)
        t1 = threading.Thread(target=client.send_command, args=(self.controller,))
        t2 = threading.Thread(target=controllerDisplay.display, args=())
        t1.start()
        t2.start()

    def getDir(self):
        
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        #dialog.setFilter("Text files (*.txt)")
        #filenames = QtGui.QStringList()

        if dialog.exec_():
            self.dirpath = dialog.directory().path() + "/"
            self.lineEdit.setText(self.dirpath)
            print(self.dirpath)
        
        


    def moveCrawler(self):
        
        self.move = MoveCrawler(self.controller, self.spinBox.value())
        self.move.start()

    def ShutdownCrawler(self):
        self.controller.shutdowncrawler = True
    
    def extendTether(self):
        self.pwmtether.start(80)
        GPIO.output(31,0)
        self.tetheron = True

    def retractTether(self):
        self.pwmtether.start(80)
        GPIO.output(31,1)
        self.tetheron = True

    def stopTether(self):
        self.pwmtether.stop()
        GPIO.output(31,0)
        self.tetheron = False

    def TakePictures(self):
        self.takePicture = True
        self.thread.TakePictures()

    def RecordVideos(self):
        _translate = QtCore.QCoreApplication.translate
        if self.recordVideo == False:
            self.pushButton_3.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.pushButton_3.setText(_translate("Form", "Stop recording"))
            self.thread.startRecording()   
            #self.recordVideo == True 
        elif self.recordVideo == True:
            self.pushButton_3.setStyleSheet("background-color: rgb(85, 255, 255);")
            self.pushButton_3.setText(_translate("Form", "Start recording"))
            self.thread.stopRecording()   
            #self.recordVideo == False
        self.recordVideo = not self.recordVideo 

    
class ControllerDisplay(): 
    #finished = pyqtSignal()  
    def __init__(self, controller, ui): 
        #super(QThread, self).__init__() 
        self.controller = controller
        self.ui = ui
        #self.label = label  

    def display(self):
        #self.ThreadActive = True
        while True:
           
            if self.controller.in1 == 1 and self.controller.in4 == 1:
                self.ui.label.show()
                self.ui.start = True
                if self.ui.comboBox.currentText() == "Backward" and self.ui.tetheron == False:
                    self.ui.pwmtether.start(45)
                    GPIO.output(31,1)
                elif self.ui.comboBox.currentText() == "Forward" and self.ui.tetheron == False:
                    self.ui.pwmtether.start(40)
                    GPIO.output(31,0) 
                    
            else:
                self.ui.label.hide()
                self.ui.start = False
                if self.ui.tetheron == False and self.controller.in2 == 0:
                    self.ui.pwmtether.stop()
                    GPIO.output(31,0)

            if self.controller.in2 == 1 and self.controller.in3 == 1:
                self.ui.label_2.show()
                if self.ui.comboBox.currentText() == "Backward" and self.ui.tetheron == False:
                    self.ui.pwmtether.start(40)
                    GPIO.output(31,0)
                elif self.ui.comboBox.currentText() == "Forward" and self.ui.tetheron == False:
                    self.ui.pwmtether.start(45)
                    GPIO.output(31,1) 
            else:
                self.ui.label_2.hide()
                if self.ui.tetheron == False and self.controller.in1 == 0:
                    self.ui.pwmtether.stop()
                    GPIO.output(31,0)
            if self.controller.in1 == 1 and self.controller.in3 == 1:
                self.ui.label_3.show()
            else:
                self.ui.label_3.hide()
            if self.controller.in2 == 1 and self.controller.in4 == 1:
                self.ui.label_4.show()
            else:
                self.ui.label_4.hide()
            if self.controller.in2 == 1 and self.controller.in4 == 1:
                self.ui.label_4.show()
            else:
                self.ui.label_4.hide()
            if self.controller.basein1 == 1:
                self.ui.label_7.show()
            else:
                self.ui.label_7.hide()
            if self.controller.basein2 == 1:
                self.ui.label_8.show()
            else:
                self.ui.label_8.hide()
            if self.controller.elbowin1 == 1:
                self.ui.label_9.show()
            else:
                self.ui.label_9.hide()
            if self.controller.elbowin2 == 1:
                self.ui.label_10.show()
            else:
                self.ui.label_10.hide()
            if self.controller.wristin2 == 1:
                self.ui.label_11.show()
            else:
                self.ui.label_11.hide()
            if self.controller.wristRight > 0:
                self.ui.label_12.show()
            else:
                self.ui.label_12.hide()
            if self.controller.wristLeft > 0:
                self.ui.label_13.show()
            else:
                self.ui.label_13.hide()
            if self.controller.wristin1 == 1:
                self.ui.label_14.show()
            else:
                self.ui.label_14.hide()
            if self.controller.gripperOpen == 1:
                self.ui.label_15.show()
            else:
                self.ui.label_15.hide()
            if self.controller.gripperClose == 1:
                self.ui.label_16.show()
            else:
                self.ui.label_16.hide()
            time.sleep(0.3)
            #self.finished.emit()

class MoveCrawler(QThread):
    finished = pyqtSignal() 

    def __init__(self, controller, t): 
        super(QThread, self).__init__() 
        self.controller = controller
        self.t = t
    
    def run(self):
        self.controller.on_up_arrow_press()
        time.sleep(self.t)
        self.controller.on_up_down_arrow_release()



class VideoThread(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, takePicture, dirpath):
        super(QThread, self).__init__()
        self.takePicture = takePicture
        self.dirpath = dirpath
        self.recordVideo = False
        self.result = None
    
    def TakePictures(self):
        self.takePicture = True

    def startRecording(self):
        size = (320, 240)
        date = datetime.now()
        videoname = date.strftime("%d%m%Y_%H_%M_%S")
        #print(str(videoname) + '.avi')
        self.result = cv2.VideoWriter(self.dirpath + str(videoname) + 'video.avi',cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
        self.recordVideo = True
        
        

    def stopRecording(self):
        self.result.release()
        self.recordVideo = False
        
    def white_balance(self, img):
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        return result

    def run(self):
        self.ThreadActive = True    
        Capture = cv2.VideoCapture('http://192.168.0.11:9000/stream.mjpg')
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                frame[...,2] = cv2.multiply(frame[...,2], 0.8)
                frame[...,0] = cv2.multiply(frame[...,0], 0.7)
                #frame = self.white_balance(frame)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                if self.takePicture == True:
                    date = datetime.now()
                    picturename = date.strftime("%d%m%Y_%H_%M_%S")
                    cv2.imwrite(self.dirpath + str(picturename) + 'picture.png', cv2.resize(frame, (1280, 720)))
                    #print(self.dirpath + str(picturename) + 'picture.png')
                    self.takePicture = False
                if self.recordVideo == True:
                    self.result.write(frame)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

