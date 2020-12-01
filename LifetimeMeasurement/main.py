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
from PyQt5.QtCore import QTimer
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


    def connectAll(self):
        # self.comboBox_laserController.currentTextChanged.connect(self.selectResources)
        self.pushButton_refresh.clicked.connect(self.refreshResources)
        self.pushButton_selectFolder.clicked.connect(self.selectFolder)
        self.pushButton_start.clicked.connect(self.startMeasure)

    # def selectResources(self):
    #     self.laserController = self.comboBox_laserController.currentText()
    #     self.oscilloscope = self.comboBox_oscilloscope.currentText()


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
        stepsDouble = steps*2
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
        self.measureEachTurn(-1,laser_controller,oscilloscope,stepsDouble,waiting_time=waiting_time,timeBetweenTurns=timeBetweenTurns)

        self.spinBox_turns.lineEdit().setEnabled(True)
        self.spinBox_acquiringTime.lineEdit().setEnabled(True)
        self.spinBox_timeBetweenTurns.lineEdit().setEnabled(True)


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
        if i<=stepsDouble:

            getDS6_rawdata_run(oscilloscope)

            QTimer.singleShot(int(timeBetweenTurns * 1e3),
                              lambda: self.measureEachTurn(i+1, laser_controller,oscilloscope,stepsDouble,
                                                           waiting_time,timeBetweenTurns))
            if i >= 0:
                self.progressBar.setValue(int(i/stepsDouble*100))
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



    def measureEachTurn1(self,i,laser_controller,oscilloscope,last_time,steps,waiting_time=6,timeBetweenTurns=10):
        curr_time = time.time()

        print("Step: " + str(i + 1) + "/" + str(steps), end="\t")
        if last_time == None:
            print("Time left: Loading")
        else:
            print("Time left: " + str(timedelta(seconds=round((curr_time - last_time) * (steps - i)))))
        last_time = time.time()
        # time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        QtTest.QTest.qWait(timeBetweenTurns*1e3)
        laser_controller.write("OUTP ON")
        rawdata_on = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # time.sleep(timeBetweenTurns)  # to make sure the controller does not turn on/off laser too frequently
        QtTest.QTest.qWait(timeBetweenTurns * 1e3)
        laser_controller.write("OUTP OFF")
        rawdata_off = getDS6_rawdata(oscilloscope, waiting_time=waiting_time)
        # onoff_list.append([rawdata_on, rawdata_off])
        return [rawdata_on, rawdata_off],last_time

if __name__ == "__main__":
    app = QApplication([])
    widget = lifetimeMeasurement()
    widget.show()
    sys.exit(app.exec_())
