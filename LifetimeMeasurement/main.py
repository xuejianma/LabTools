"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""

# This Python file uses the following encoding: utf-8
import sys
import os
import time
import numpy as np

from datetime import timedelta

from pyvisa import ResourceManager

from PyQt5 import uic,QtTest
from PyQt5.QtWidgets import QApplication, QWidget,QFrame, QFileDialog
from PyQt5.QtCore import QTimer,QThread
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
        # print(__file__)
    def refreshResources(self):
        self.comboBox_laserController.clear()
        self.comboBox_oscilloscope.clear()
        self.listResources()

    def selectFolder(self):
        filename = QFileDialog.getExistingDirectory(self,'select directory')
        self.lineEdit_folder.setText(filename)

    def startMeasure(self):
        laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        oscilloscope = self.rm.open_resource(self.comboBox_oscilloscope.currentText())
        steps = self.spinBox_turns.value()
        self.stepsDouble = steps*2
        waiting_time = self.spinBox_acquiringTime.value()
        timeBetweenTurns = self.spinBox_timeBetweenTurns.value()

        self.spinBox_turns.setEnabled(False)
        self.spinBox_acquiringTime.setEnabled(False)
        self.spinBox_timeBetweenTurns.setEnabled(False)

        print(steps,waiting_time,timeBetweenTurns)
        # onoff_list = repeat(laser_controller, oscilloscope, steps = 10, waiting_time = 6)

        last_time = None
        onoff_list = []
        # for i in range(steps):
        #     [rawdata_on, rawdata_off],last_time = self.measureEachTurn1(i,laser_controller,oscilloscope,last_time,steps,waiting_time=waiting_time,timeBetweenTurns=timeBetweenTurns)
        #     currentDecay = np.asarray([item1-item2 for item1,item2 in zip(rawdata_on,rawdata_off)])
        #     self.widget_currentDecay.plot(currentDecay)

        self.timeLeft = int((self.stepsDouble) * (waiting_time + timeBetweenTurns))-timeBetweenTurns
        print(self.timeLeft)
        self.countdown(intervalSecond=1)
        self.progressBar.setValue(0)
        self.on_list=[]
        self.off_list=[]

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
        # rawdata = oscilloscope.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
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
        newtime = time.strftime('%H : %M : %S', time.gmtime(self.timeLeft))
        self.label_countdown.setText("Time Left:    " + newtime + " (hh : mm : ss)")
        print(newtime)
        if self.timeLeft == 0:
            self.timerCountdown.stop()
        # "Time Left:    00 : 00 : 00 (hh : mm : ss)"


    def getDS6_rawdata_stop(self):
        return getDS6_rawdata_stop()


    def measureOn(self,laser_controller,oscilloscope,waiting_time):
        # rawdata_on = []
        laser_controller.write("OUTP ON")
        # getDS6_rawdata_run(oscilloscope)
        # print(waiting_time)
        # time1 = time.time()
        QTimer.singleShot(int(waiting_time*1e3),lambda:getDS6_rawdata_stop(oscilloscope, rawdata_list=self.on_list))
        # rawdata_on = getDS6_rawdata_stop(oscilloscope)
        # time2 = time.time()
        # print(time2-time1)
        # print(rawdata_on)
        # rawdata_on = getDS6_rawdata_stop(oscilloscope, waiting_time=waiting_time)
        # return rawdata_on

    def measureOff(self,laser_controller,oscilloscope,waiting_time):
        # rawdata_off = []
        laser_controller.write("OUTP OFF")
        # getDS6_rawdata_run(oscilloscope)
        QTimer.singleShot(int(waiting_time*1e3),lambda:getDS6_rawdata_stop(oscilloscope, rawdata_list=self.off_list))
        # rawdata_off = getDS6_rawdata_stop(oscilloscope)
        # rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # return rawdata_off


        QTimer.singleShot(int(waiting_time * 1e3)+int(0.5e3),self.plotDecay)

    def plotDecay(self):
        currentDecay = np.asarray([item1 - item2 for item1, item2 in zip(self.on_list[-1], self.off_list[-1])])
        self.widget_currentDecay.clear()
        self.widget_currentDecay.plot(currentDecay)




    def measureEachTurn(self,i,laser_controller,oscilloscope,stepsDouble,waiting_time,timeBetweenTurns):
        if i<stepsDouble:

            getDS6_rawdata_run(oscilloscope)

            QTimer.singleShot(int(timeBetweenTurns * 1e3),
                              lambda: self.measureEachTurn(i+1, laser_controller,oscilloscope,stepsDouble,
                                                           waiting_time,timeBetweenTurns+waiting_time))
            if i >= 0:

                if i%2==0:
                    self.measureOn(laser_controller, oscilloscope,waiting_time=waiting_time)
                    # self.on_list.append(rawdata_on)
                    # print(i)
                    # print(self.on_list)
                else:
                    self.measureOff(laser_controller, oscilloscope,waiting_time=waiting_time)
                    # self.on_list.append(rawdata_off)
                    # print(i)
                    # print(self.off_list)
                    # currentDecay = np.asarray([item1 - item2 for item1, item2 in zip(self.on_list[-1], self.off_list[-1])])
                    # self.widget_currentDecay.plot(currentDecay)
                QTimer.singleShot(int(waiting_time * 1e3),lambda:self.progressBar.setValue(int((i + 1) / stepsDouble * 100)))



    def measureEachTurn1(self,i,laser_controller,oscilloscope,last_time,steps,waiting_time=6,timeBetweenTurns=10):
        curr_time = time.time()

        print("Step: " + str(i + 1) + "/" + str(steps), end="\t")
        if last_time == None:
            print("Time left: Loading")
        else:
            print("Time left: " + str(timedelta(seconds=round((curr_time - last_time) * (steps - i)))))
        last_time = time.time()
        time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        # QtTest.QTest.qWait(timeBetweenTurns*1e3)
        QThread.sleep(timeBetweenTurns)
        laser_controller.write("OUTP ON")
        # rawdata_on = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        # QtTest.QTest.qWait(timeBetweenTurns * 1e3)
        QThread.sleep(timeBetweenTurns)

        laser_controller.write("OUTP OFF")
        # rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # onoff_list.append([rawdata_on, rawdata_off])
        # return [rawdata_on, rawdata_off],last_time

if __name__ == "__main__":
    app = QApplication([])
    widget = lifetimeMeasurement()
    widget.show()
    sys.exit(app.exec_())
