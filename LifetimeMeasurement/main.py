"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""

# This Python file uses the following encoding: utf-8
import sys
import os
import time
import numpy as np
from pandas import DataFrame

from datetime import timedelta

from pyvisa import ResourceManager

from PyQt5 import uic,QtTest
from PyQt5.QtWidgets import QApplication, QWidget,QFrame, QFileDialog
from PyQt5.QtCore import QTimer,QThread,QProcess
# from PyQt5.QtUiTools import QUiLoader
from utils import getDS6_rawdata,getDS6_rawdata_run,getDS6_rawdata_stop


class lifetimeMeasurement(QWidget):
    def __init__(self):
        super(lifetimeMeasurement, self).__init__()
        self.load_ui()
        self.connectAll()

        self.rm = ResourceManager()
        self.listResources()


        # self.laserController = None
        # self.oscilloscope = None
        self.widget_currentDecay.setBackground('w')
        self.widget_averagedDecay.setBackground('w')
        self.widget_currentDecay.setFrameShape(QFrame.Box)
        self.widget_averagedDecay.setFrameShape(QFrame.Box)

        self.on_list = []
        self.off_list = []
        self.timerCountdown = None
        self.timeLeft = None


    def connectAll(self):
        # self.comboBox_laserController.currentTextChanged.connect(self.selectResources)
        self.pushButton_refresh.clicked.connect(self.refreshResources)
        self.pushButton_selectFolder.clicked.connect(self.selectFolder)
        self.pushButton_start.clicked.connect(self.startMeasure)
        self.pushButton_tmp.clicked.connect(self.clickTmp)

    # def selectResources(self):
    #     self.laserController = self.comboBox_laserController.currentText()
    #     self.oscilloscope = self.comboBox_oscilloscope.currentText()

    def clickTmp(self):
        print('on: ',np.shape(self.on_list))
        print('off',np.shape(self.off_list))

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__),"form.ui")
        uic.loadUi(path,self)

    def listResources(self):

        usb_list = self.rm.list_resources()
        print(usb_list)
        for item in usb_list:
            self.comboBox_laserController.addItem(item)
            self.comboBox_oscilloscope.addItem(item)
            if "DS6D150100004" in item:
                self.comboBox_oscilloscope.setCurrentText(item)  # find and define oscilloscope USB port
            elif "M00460823" in item:
                self.comboBox_laserController.setCurrentText(item)  # find and define laser controller USB port

        # print(__file__)
    def refreshResources(self):
        self.comboBox_laserController.clear()
        self.comboBox_oscilloscope.clear()
        self.listResources()

    def selectFolder(self):
        filename = QFileDialog.getExistingDirectory(self,'select directory')
        self.lineEdit_folder.setText(filename)

    # def abort(self):
    #     pass

    def startMeasure(self):
        laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        oscilloscope = self.rm.open_resource(self.comboBox_oscilloscope.currentText())
        self.steps = self.spinBox_turns.value()
        self.stepsDouble = self.steps*2
        waiting_time = self.spinBox_acquiringTime.value()
        timeBetweenTurns = self.spinBox_timeBetweenTurns.value()

        self.spinBox_turns.setEnabled(False)
        self.spinBox_acquiringTime.setEnabled(False)
        self.spinBox_timeBetweenTurns.setEnabled(False)
        # self.pushButton_start.setText('Abort')




        # self.process = QProcess(self)
        # # QProcess emits `readyRead` when there is data to be read
        # self.process.readyRead.connect(self.dataReady)
        # self.runButton1.clicked.connect(self.process.kill)



        print(self.steps,waiting_time,timeBetweenTurns)

        self.label_turnsLeft.setText('Turns Finished: 0/'+str(self.steps))

        self.totalTime = int((self.stepsDouble) * (waiting_time + timeBetweenTurns))-timeBetweenTurns+1
        self.timeLeft = self.totalTime
        print(self.timeLeft)
        self.countdown(intervalSecond=1)
        self.progressBar.setValue(0)
        self.on_list = []
        self.off_list = []

        # self.measureEachTurn(-1,laser_controller,oscilloscope,stepsDouble,waiting_time=waiting_time,timeBetweenTurns=timeBetweenTurns)

        self.timerLaserControl = QTimer()
        self.timerOscilloscopeRun = QTimer()
        self.timerOscilloscopeStop = QTimer()
        #
        self.currTurn = 0
        #
        self.timerLaserControl.timeout.connect(lambda:self.laserControl(laser_controller))
        self.timerOscilloscopeRun.timeout.connect(lambda:self.oscilloscopeRun(oscilloscope))
        self.timerOscilloscopeStop.timeout.connect(lambda:self.oscilloscopeStop(oscilloscope))

        self.laserControl(laser_controller)
        self.oscilloscopeRun(oscilloscope)
        QTimer.singleShot(int(waiting_time*1e3),lambda:self.oscilloscopeStop(oscilloscope))


        self.timerLaserControl.start(int((waiting_time+timeBetweenTurns)*1e3))
        self.timerOscilloscopeRun.start(int((waiting_time+timeBetweenTurns)*1e3))
        QTimer.singleShot(int(waiting_time*1e3),lambda:self.timerOscilloscopeStop.start(int((waiting_time+timeBetweenTurns)*1e3)))


        self.spinBox_turns.lineEdit().setEnabled(True)
        self.spinBox_acquiringTime.lineEdit().setEnabled(True)
        self.spinBox_timeBetweenTurns.lineEdit().setEnabled(True)

    def laserControl(self,laser_controller):
        if self.currTurn % 2 == 0:
            laser_controller.write("OUTP ON")
            print('laser on')
        else:
            laser_controller.write("OUTP OFF")
            print('laser off')

    def oscilloscopeRun(self,oscilloscope):
        oscilloscope.write(":RUN")
        print('oscilloscopeRun')

    def oscilloscopeStop(self,oscilloscope ,start=1, points=70000000,):
        if self.currTurn == self.stepsDouble-1:
            self.timerLaserControl.stop()
            self.timerOscilloscopeRun.stop()
            self.timerOscilloscopeStop.stop()

        wt = 0;
        oscilloscope.write(":STOP")
        oscilloscope.write(":WAV:MODE NORM")  # RAW means deeper raw data. NORM means displayed data
        time.sleep(wt)
        oscilloscope.write(":WAV:STAR " + str(start))
        time.sleep(wt)
        oscilloscope.write(":WAV:STOP " + str(points + start))
        time.sleep(wt)
        oscilloscope.write(":WAV:POIN " + str(points))
        time.sleep(wt)
        oscilloscope.write(":WAV:SOUR CHAN1")
        time.sleep(wt)
        oscilloscope.write(":WAV:RES")
        time.sleep(wt)
        oscilloscope.write(":WAV:BEG")
        time.sleep(wt)
        rawdata = oscilloscope.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
        if self.currTurn % 2 == 0:
            self.on_list.append(rawdata)
            print('onlist append')
        else:
            self.off_list.append(rawdata)
            print('offlist append')
            self.label_turnsLeft.setText('Turns Finished: ' + str(int(np.floor((self.currTurn+1)/2))) + '/' + str(int(self.steps)))
            QTimer.singleShot(500,self.plotDecay)
            QTimer.singleShot(500,lambda:print('plotDecay'))

        self.currTurn += 1
        print('oscilloscopeStop')

    def countdown(self,intervalSecond):

        self.timerCountdown = QTimer()
        # print(123)
        self.timerCountdown.timeout.connect(lambda:self.updateCountdown(intervalSecond))
        self.timerCountdown.start(int(intervalSecond*1e3))
        # print(456)

    def updateCountdown(self,intervalSecond):
        self.timeLeft -= intervalSecond
        self.progressBar.setValue(int((self.totalTime-self.timeLeft)/self.totalTime*100))
        newtime = time.strftime('%H : %M : %S', time.gmtime(self.timeLeft))
        self.label_countdown.setText("Time Left:    " + newtime + " (hh : mm : ss)")
        print(newtime)
        if self.timeLeft == 0:
            self.timerCountdown.stop()
        # "Time Left:    00 : 00 : 00 (hh : mm : ss)"

    def plotDecay(self):
        currentDecay = np.asarray([item1 - item2 for item1, item2 in zip(self.on_list[-1], self.off_list[-1])])
        self.widget_currentDecay.clear()
        self.widget_currentDecay.plot(currentDecay)

        on_mean = np.mean(self.on_list, axis=0)
        off_mean = np.mean(self.off_list, axis=0)
        averagedDecay = np.array([item1 - item2 for item1, item2 in zip(on_mean, off_mean)])
        self.widget_averagedDecay.clear()
        self.widget_averagedDecay.plot(averagedDecay)

        path = self.lineEdit_folder.text()
        filename = self.lineEdit_file.text()
        self.saveFiles(path,filename,self.on_list,self.off_list,averagedDecay)

    def saveFiles(self,path,filename,rawdata_on,rawdata_off,averaged):

        df1 = DataFrame(rawdata_on).T
        df2 = DataFrame(rawdata_off).T
        df3 = DataFrame(averaged)

        df1.to_csv(path+'/'+filename+'_on.csv')
        df2.to_csv(path + '/' + filename + '_off.csv')
        df3.to_csv(path + '/' + filename + '_averaged.csv')






if __name__ == "__main__":
    app = QApplication([])
    widget = lifetimeMeasurement()
    widget.show()
    sys.exit(app.exec_())
