"""
Created by Xuejian Ma at 11/30/2020.
All rights reserved.
"""

# This Python file uses the following encoding: utf-8
import sys
import os
import time
import numpy as np
from pandas import DataFrame, read_csv

from datetime import timedelta

from pyvisa import ResourceManager

from PyQt5 import uic,QtTest
from PyQt5.QtWidgets import QApplication, QWidget,QFrame, QFileDialog,QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QTimer,QThread,QProcess
from utils import decay1,decay2,decay3,normalize,denormalize
from scipy.optimize import curve_fit
from pyqtgraph import mkPen

# from PyQt5.QtUiTools import QUiLoader
# from utils import getDS6_rawdata,getDS6_rawdata_run,getDS6_rawdata_stop


class lifetimeMeasurement(QWidget):
    def __init__(self):
        super(lifetimeMeasurement, self).__init__()
        self.load_ui()
        self.connectAll()

        self.rm = ResourceManager()
        self.listResources()
        # self.laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        # self.oscilloscope = self.rm.open_resource(self.comboBox_oscilloscope.currentText())

        # self.laserController = None
        # self.oscilloscope = None
        self.widget_currentDecay.setBackground('w')
        self.widget_averagedDecay.setBackground('w')
        self.widget_fitting.setBackground('w')
        self.widget_currentDecay.setFrameShape(QFrame.Box)
        self.widget_averagedDecay.setFrameShape(QFrame.Box)
        self.widget_fitting.setFrameShape(QFrame.Box)

        self.on_list = []
        self.off_list = []
        self.averagedDecay = []
        self.xaxis = []
        self.current_list = []
        self.power_list = []
        self.timerCountdown = None
        self.timeLeft = None
        self.dataLoadedX = None
        self.dataLoadedY = None
        self.yFitted = None
        self.xFitReal = None
        self.scanCurrent = 0.




    def connectAll(self):
        # self.comboBox_laserController.currentTextChanged.connect(self.selectResources)
        self.pushButton_refresh.clicked.connect(self.refreshResources)
        self.pushButton_powerMeter.clicked.connect(self.refreshResourcesPowerMeter)
        self.pushButton_selectFolder.clicked.connect(self.selectFolder)
        self.pushButton_start.clicked.connect(self.startMeasure)
        self.pushButton_tmp.clicked.connect(self.clickTmp)
        # without singleShot, weird error occurs for pyvisa self.rm.open_resource for oscilloscope
        self.comboBox_laserController.currentIndexChanged.connect(lambda:QTimer.singleShot(0,self.updateResources))
        # without singleShot, weird error occurs for pyvisa self.rm.open_resource for oscilloscope
        self.comboBox_oscilloscope.currentIndexChanged.connect(lambda:QTimer.singleShot(0,self.updateResources))
        self.comboBox_powerMeter.currentIndexChanged.connect(lambda: QTimer.singleShot(0, self.updateResourcesPowerMeter))
        self.pushButton_laserOn.clicked.connect(lambda:self.laser_controller.write("OUTP ON"))
        self.pushButton_laserOff.clicked.connect(lambda: self.laser_controller.write("OUTP OFF"))
        self.lineEdit_setpoint.editingFinished.connect(self.currentSetpoint)
        self.pushButton_selectFileFit.clicked.connect(self.selectFileFit)
        self.pushButton_fromFile.clicked.connect(self.loadDataFromCsv)
        self.pushButton_fromMeasurement.clicked.connect(self.loadDataFromMeasurement)
        self.pushButton_fitDecay.clicked.connect(self.fitDecay)
        self.pushButton_saveFittedCurve.clicked.connect(self.saveFittedCurve)
        self.pushButton_startScanning.clicked.connect(self.startScanning)
        self.pushButton_scanFromMeasure.clicked.connect(self.loadScanDataFromMeasurement)
        self.pushButton_scanSave.clicked.connect(self.saveScanData)
        self.pushButton_scanFromFile.clicked.connect(self.loadScanDataFromFile)
        self.pushButton_scanFromMeasure_2.clicked.connect(self.loadScanDataFromMeasurement2)
        self.pushButton_scanFromFile_2.clicked.connect(self.loadScanDataFromFile2)
    # def selectResources(self):
    #     self.laserController = self.comboBox_laserController.currentText()
    #     self.oscilloscope = self.comboBox_oscilloscope.currentText()

    def clickTmp(self):
        print('on: ',np.shape(self.on_list))
        print('off: ',np.shape(self.off_list))

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__),"form.ui")
        uic.loadUi(path,self)

    def listResources(self):

        usb_list = self.rm.list_resources()
        print(usb_list)
        for item in usb_list:
            self.comboBox_laserController.addItem(item)
            self.comboBox_oscilloscope.addItem(item)
            self.comboBox_powerMeter.addItem(item)
            if "DS6D150100004" in item:
                self.comboBox_oscilloscope.setCurrentText(item)  # find and define oscilloscope USB port
            elif "M00460823" in item:
                self.comboBox_laserController.setCurrentText(item)  # find and define laser controller USB port
            elif "P0016683" in item:
                self.comboBox_powerMeter.setCurrentText(item)  # find and define laser controller USB port

        # print(__file__)
    def refreshResources(self):
        self.comboBox_laserController.clear()
        self.comboBox_oscilloscope.clear()
        self.listResources()

    def refreshResourcesPowerMeter(self):
        self.comboBox_powerMeter.clear()
        self.listResources()

    def selectFolder(self):
        filename = QFileDialog.getExistingDirectory(self,'select directory')
        self.lineEdit_folder.setText(filename)

    # def abort(self):
    #     pass
    
    def updateResources(self):
        # self.rm.close()
        # self.rm = ResourceManager()
        # print(self.comboBox_laserController.currentText())

        self.laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        # print(self.comboBox_oscilloscope.currentText())
        self.oscilloscope = self.rm.open_resource(self.comboBox_oscilloscope.currentText())
        print('update resources: laser_controller:',self.comboBox_laserController.currentText(),' oscilloscope:',self.comboBox_oscilloscope.currentText())

    def updateResourcesPowerMeter(self):
        self.powerMeter = self.rm.open_resource(self.comboBox_powerMeter.currentText())
        print('update resources: powerMeter:',self.comboBox_powerMeter.currentText())


    def currentSetpoint(self):
        currSetpoint = self.lineEdit_setpoint.text()
        try:
            currSetpointValue = int(currSetpoint)
            print(currSetpointValue)
            self.laser_controller.write("SOUR:CURR {}".format(currSetpointValue / 1e4))
        except:
            self.lineEdit_setpoint.editingFinished.disconnect()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Laser Current Setpoint must be integers")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Warning")
            # msg.setDetailedText("The details are as follows:")
            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(msgbtn)
            msg.exec_()
            self.lineEdit_setpoint.editingFinished.connect(self.currentSetpoint)
            # print
            # "value of pressed message box button:", retval


    def startMeasure(self):
        # self.rm.close()
        # self.rm = ResourceManager()
        self.laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        self.oscilloscope = self.rm.open_resource(self.comboBox_oscilloscope.currentText())
        self.steps = self.spinBox_turns.value()
        self.stepsDouble = self.steps*2
        waiting_time = self.spinBox_acquiringTime.value()
        timeBetweenTurns = self.spinBox_timeBetweenTurns.value()

        self.spinBox_turns.setEnabled(False)
        self.spinBox_acquiringTime.setEnabled(False)
        self.spinBox_timeBetweenTurns.setEnabled(False)
        self.spinBox_xaxis.setEnabled(False)
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
        self.timerLaserControl.timeout.connect(lambda:self.laserControl(self.laser_controller))
        self.timerOscilloscopeRun.timeout.connect(lambda:self.oscilloscopeRun(self.oscilloscope))
        self.timerOscilloscopeStop.timeout.connect(lambda:self.oscilloscopeStop(self.oscilloscope))

        self.laserControl(self.laser_controller)
        self.oscilloscopeRun(self.oscilloscope)
        QTimer.singleShot(int(waiting_time*1e3),lambda:self.oscilloscopeStop(self.oscilloscope))


        self.timerLaserControl.start(int((waiting_time+timeBetweenTurns)*1e3))
        self.timerOscilloscopeRun.start(int((waiting_time+timeBetweenTurns)*1e3))
        QTimer.singleShot(int(waiting_time*1e3),lambda:self.timerOscilloscopeStop.start(int((waiting_time+timeBetweenTurns)*1e3)))

        QTimer.singleShot(int((self.totalTime)*1e3),self.restartSpinBoxes)

    def restartSpinBoxes(self):
        self.spinBox_turns.setEnabled(True)
        self.spinBox_acquiringTime.setEnabled(True)
        self.spinBox_timeBetweenTurns.setEnabled(True)
        self.spinBox_xaxis.setEnabled(True)

    def laserControl(self,laser_controller):
        # print(self.currTurn)
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
            print('stop properly')
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
        unitTime = int(self.spinBox_xaxis.value())
        currentDecay = np.asarray([item1 - item2 for item1, item2 in zip(self.on_list[-1], self.off_list[-1])])
        self.widget_currentDecay.clear()
        self.xaxis = unitTime*14/len(currentDecay)*np.asarray(range(len(currentDecay)))
        self.widget_currentDecay.plot(self.xaxis,currentDecay)

        on_mean = np.mean(self.on_list, axis=0)
        off_mean = np.mean(self.off_list, axis=0)
        self.averagedDecay = np.array([item1 - item2 for item1, item2 in zip(on_mean, off_mean)])
        self.widget_averagedDecay.clear()
        self.widget_averagedDecay.plot(self.xaxis,self.averagedDecay)

        path = self.lineEdit_folder.text()
        filename = self.lineEdit_file.text()
        self.saveFiles(path,filename,self.on_list,self.off_list,self.averagedDecay,self.xaxis)

    def saveFiles(self,path,filename,rawdata_on,rawdata_off,averaged,xaxis):

        df1 = DataFrame(rawdata_on).T
        df2 = DataFrame(rawdata_off).T
        df3 = DataFrame(averaged)
        df1 = df1.rename(columns={0: 'signal'})
        df2 = df2.rename(columns={0: 'signal'})
        df3 = df3.rename(columns={0: 'signal'})
        df1.index = xaxis
        df2.index = xaxis
        df3.index = xaxis
        df1.index.name = 'Time(ns)'
        df2.index.name = 'Time(ns)'
        df3.index.name = 'Time(ns)'

        df1.to_csv(path+'/'+filename+'_on.csv')
        df2.to_csv(path + '/' + filename + '_off.csv')
        df3.to_csv(path + '/' + filename + '_averaged.csv')

    def selectFileFit(self):
        filename,_ = QFileDialog.getOpenFileName(self,'select *_averaged.csv file')
        self.lineEdit_selectFileFit.setText(filename)

    def loadDataFromCsv(self):
        self.widget_fitting.clear()
        dataLoaded = read_csv(self.lineEdit_selectFileFit.text(),index_col=0)
        self.dataLoadedX = np.asarray(dataLoaded.index)
        if self.checkBox_inversed.isChecked():
            self.dataLoadedY = -np.asarray(dataLoaded['signal'])
        else:
            self.dataLoadedY = np.asarray(dataLoaded['signal'])
        # print(self.dataLoaded)
        self.widget_fitting.plot(self.dataLoadedX,self.dataLoadedY)

    def loadDataFromMeasurement(self):
        self.widget_fitting.clear()
        self.dataLoadedX = self.xaxis
        if self.checkBox_inversed.isChecked():
            self.dataLoadedY = -self.averagedDecay
        else:
            self.dataLoadedY = self.averagedDecay
        self.widget_fitting.plot(self.dataLoadedX, self.dataLoadedY)

    def fitDecay(self):
        self.widget_fitting.clear()
        self.widget_fitting.plot(self.dataLoadedX, self.dataLoadedY)
        if self.radioButton_decay1.isChecked():
            decay = decay1
            bounds = [[0,0,-np.inf],np.inf]
        elif self.radioButton_decay2.isChecked():
            decay = decay2
            bounds = [[0, 0, 0, 0, -np.inf], np.inf]
        elif self.radioButton_decay3.isChecked():
            decay = decay3
            bounds = [[0, 0, 0, 0, 0, 0, -np.inf], np.inf]
        starting = self.doubleSpinBox_starting.value()
        ending = self.doubleSpinBox_ending.value()
        selectedIndices = np.where(np.logical_and(self.dataLoadedX>starting,self.dataLoadedX<ending))[0]
        xSelected = self.dataLoadedX[selectedIndices]
        ySelected = self.dataLoadedY[selectedIndices]
        xFit = normalize(xSelected)
        params, corrs = curve_fit(decay, xFit, ySelected,bounds=bounds)
        self.yFitted = decay(xFit, *params)
        self.xFitReal = np.round(denormalize(xFit,xSelected),2)
        self.widget_fitting.plot(self.xFitReal,self.yFitted,pen=mkPen(color='r'))

        if decay == decay1:
            self.textBrowser_result.setText(
                'A=' + str(np.round(params[0],5)) + ', t=' + str(np.round(denormalize(params[1],xSelected),5)) +
                ', y0=' + str(np.round(params[2],5)))
        elif decay == decay2:
            # paramIndices = np.argsort([params[1],params[2]])
            self.textBrowser_result.setText(
                'A1=' + str(np.round(params[0],5)) + ', A2=' + str(np.round(params[1],5)) + ', t1='
                + str(np.round(denormalize(params[2],xSelected),5))
                +', t2=' + str(np.round(denormalize(params[3],xSelected),5)) + ', y0=' + str(np.round(params[4],5)))
        elif decay == decay3:
            self.textBrowser_result.setText(
                'A1=' + str(np.round(params[0], 5)) + ', A2=' + str(np.round(params[1], 5)) + ', A3=' +
                str(np.round(params[2], 5))+', t1=' + str(np.round(denormalize(params[3], xSelected), 5))
                + ', t2=' + str(np.round(denormalize(params[4], xSelected), 5)) +
                ', t3=' + str(np.round(denormalize(params[5], xSelected), 5))+', y0=' + str(np.round(params[6], 5)))

    def saveFittedCurve(self):
        path = QFileDialog.getSaveFileName(self,'Save Fitted Curve with Data','./',"csv Files (*.csv);;All Files (*)")[0]
        df1 = DataFrame(self.dataLoadedY).rename(columns={0:'signal'})
        df1.index = self.dataLoadedX
        df2 = DataFrame(self.yFitted).rename(columns={0:'fitting'})
        df2.index = self.xFitReal
        df = df1.join(df2)
        df.index.name = 'Time(ns)'
        print(path)
        # print(df)
        df.to_csv(path)

    def startScanning(self):
        self.tableWidget_scanCurrent.setRowCount(0)
        self.progressBar_currentScan.setValue(0)
        self.current_list = []
        self.power_list = []
        self.laser_controller = self.rm.open_resource(self.comboBox_laserController.currentText())
        self.powerMeter = self.rm.open_resource(self.comboBox_powerMeter.currentText())

        starting = self.spinBox_currentStart.value()*1e-4
        self.scanCurrent = np.round(starting,6)
        ending = self.spinBox_currentEnd.value()*1e-4
        steps = self.spinBox_currentSteps.value()
        currentDelta = float(ending-starting)/steps
        time = self.spinBox_currentTime.value()
        step_time = int(float(time)/steps*1e3)
        self.tmpIndexScan = 0
        self.scanTimer = QTimer()
        self.scanTimer.timeout.connect(lambda:self.getPower(currentDelta,self.current_list,self.power_list,starting,ending,steps))
        self.scanTimer.start(step_time)
        print('scanning started',self.scanTimer)

    def getPower(self,currentDelta,current_list,power_list,starting,ending,steps):
        flag = False
        if self.tmpIndexScan>=steps:#self.scanCurrent>ending:
            self.scanTimer.stop()
            self.progressBar_currentScan.setValue(100)
            flag=True
            # del self.tmpIndexScan
        # current input
        self.laser_controller.write("SOUR:CURR {}".format(self.scanCurrent))
        power = self.powerMeter.query('Measure:Scalar:POWer?')
        self.tableWidget_scanCurrent.insertRow(self.tableWidget_scanCurrent.rowCount())
        self.tableWidget_scanCurrent.setItem(self.tmpIndexScan, 0, QTableWidgetItem(str(int(self.scanCurrent * 1e4))))
        self.tableWidget_scanCurrent.setItem(self.tmpIndexScan, 1, QTableWidgetItem(str(float(power)*1e6)))
        current_list.append(np.float(self.scanCurrent))
        power_list.append(np.float(power))
        self.scanCurrent += currentDelta
        self.scanCurrent = np.round(self.scanCurrent, 6)
        self.tmpIndexScan += 1

        self.progressBar_currentScan.setValue(int((self.scanCurrent-starting)/(ending-starting)*100))
      
        if flag==True:#self.scanCurrent>ending:
            self.laser_controller.write("SOUR:CURR {}".format(0))
        print(self.scanCurrent,power)

    def fillScanTable(self,tableWidget,scan_current_list,scan_power_list):
        tableWidget.setRowCount(0)
        tableWidget.setRowCount(len(scan_current_list))
        for ind in range(len(scan_current_list)):
            tableWidget.setItem(ind, 0, QTableWidgetItem(str(int(scan_current_list[ind] * 1e4))))
            tableWidget.setItem(ind, 1, QTableWidgetItem(str(float(scan_power_list[ind]) * 1e6)))

    def loadScanDataFromMeasurement(self):
        self.fillScanTable(self.tableWidget_scanCurrent,self.current_list,self.power_list)

    def loadScanDataFromMeasurement2(self):
        self.fillScanTable(self.tableWidget_scanCurrent_2,self.current_list,self.power_list)

    def saveScanData(self):
        path = QFileDialog.getSaveFileName(self,'Save Measured Powers with Currents','./',"csv Files (*.csv);;All Files (*)")[0]
        df = DataFrame({'Current (A)':self.current_list,'Power (W)':self.power_list})
        df.to_csv(path,index=False)

    def loadScanDataFromFile(self):
        path = QFileDialog.getOpenFileName(self,'Selected Saved *csv File')[0]
        df = read_csv(path,index_col=None)
        file_current_list = df.iloc[:,0].values
        file_power_list = df.iloc[:,1].values
        self.fillScanTable(self.tableWidget_scanCurrent, file_current_list, file_power_list)

    def loadScanDataFromFile2(self):
        path = QFileDialog.getOpenFileName(self,'Selected Saved *csv File')[0]
        df = read_csv(path,index_col=None)
        file_current_list = df.iloc[:,0].values
        file_power_list = df.iloc[:,1].values
        self.fillScanTable(self.tableWidget_scanCurrent_2, file_current_list, file_power_list)

    # def test(self):
    #     print('test')



        #       self.timerCountdown.timeout.connect(lambda:self.updateCountdown(intervalSecond))
        #       self.timerCountdown.start(int(intervalSecond*1e3))

        


if __name__ == "__main__":
    app = QApplication([])
    widget = lifetimeMeasurement()
    widget.show()
    sys.exit(app.exec_())
