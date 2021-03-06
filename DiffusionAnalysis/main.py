# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QFile, Qt, QSize, QObject, QThread, pyqtSignal
# from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap,QImage, QPainter, QPen, QBrush, QPolygon
import pyqtgraph as pg
from utils import readSimulatedImReCSV,readImRePhase,diffusion_map,radialAverageByLinecuts,radialAverage, readTXT, calibrate_xlist, calibrate_ylist, resample
from PIL import Image
# import randomQtUiTools
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyParkTiff import SaveParkTiff


class gui(QWidget):
    def __init__(self):
        super(gui, self).__init__()
        self.load_ui()
        # self.extraConfiguration()
        self.connectAll()
        self.center = QPolygon()
        self.piximg = None
        # directoryName = None
        # responseFile = None
        self.widget_response.setBackground('w')
        # self.widget_laserScreenshot.setBackground('w')
        self.widget_laserFit.setBackground('w')
        self.im_sim_raw = None
        self.re_sim_raw = None
        self.cond_array = None
        self.im_sim = None
        self.re_sim = None
        # self.laserScreenshot = None

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)

    def connectAll(self):
        self.pushButton_directory.clicked.connect(self.selectDirectory)
        # self.label_image.mousePressEvent = self.findDotPos
        # self.pushButton_tmp.clicked.connect(self.combineSubDirectories)
        self.pushButton_response.clicked.connect(self.selectResponse)
        # self.pushButton_draw.clicked.connect(self.update_graph)
        # self.pushButton_scatter.clicked.connect(self.plotResponse)
        self.pushButton_plotResponse.clicked.connect(self.plotResponse)
        self.pushButton_laserScreenshot.clicked.connect(self.selectLaserScreenshot)
        self.pushButton_laserFit.clicked.connect(self.plotLaserFit)
        self.pushButton_laserFitClear.clicked.connect(self.widget_laserFit.clear)
        self.pushButton_plotImage.clicked.connect(self.plotLaserScreenshot)
        # self.label_laserScreenshot.mousePressEvent = self.findDotPos
        # self.label_laserScreenshot.paintEvent = self.paintEvent2
        self.pushButton_laserLinecut.clicked.connect(self.plotLaserLinecut)
        self.pushButton_selectCalibrationPreviewFile.clicked.connect(self.selectCalibratedPreviewTxt)
        self.pushButton_plotCalibrationPreview.clicked.connect(self.plotCalibrationPreviewRawData)
        self.pushButton_plotCalibrationPreviewCalibrated.clicked.connect(self.plotCalibrationPreviewCalibrated)
        self.lineEdit_directory_2.setText(self.lineEdit_directory.text())
        self.lineEdit_subdirectories_2.setText(self.lineEdit_subdirectories.text())
        self.lineEdit_directory.textChanged.connect(lambda: self.lineEdit_directory_2.setText(self.lineEdit_directory.text()))
        self.lineEdit_subdirectories.textChanged.connect(lambda: self.lineEdit_subdirectories_2.setText(self.lineEdit_subdirectories.text()))
        self.pushButton_calibrateAll.clicked.connect(self.calibrateAll);
        self.pushButton_calibrateAllStop.clicked.connect(self.calibrateAllStop);
        self.lineEdit_calibrateAllFiles.setText(','.join([self.lineEdit_im.text(), self.lineEdit_re.text()]))
        self.lineEdit_im.textChanged.connect(lambda: self.lineEdit_calibrateAllFiles.setText(','.join([self.lineEdit_im.text(), self.lineEdit_re.text()])))
        self.lineEdit_re.textChanged.connect(lambda: self.lineEdit_calibrateAllFiles.setText(','.join([self.lineEdit_im.text(), self.lineEdit_re.text()])))

        #dk
    def selectDirectory(self):
        directoryName = QFileDialog.getExistingDirectory(self, 'Select directory')#getOpenFileName(self, 'Open file', '.', '')
        self.lineEdit_directory.setText(directoryName)
        # self.image = QImage()
        # self.image.load(filename) # another way to import image

        # pixtmp = QPixmap(directoryName)
        # self.piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        # self.label_image.setPixmap(self.piximg)#QPixmap.fromImage(self.image))



    # def combineSubDirectories(self):
    #     print(self.lineEdit_subdirectories.text())

    # def plotScatters(self):

        # self.widget_response.plot(im_all, re_all, pen=None,symbol = 'o',symbolPen = pg.mkPen(color=(0, 0, 255), width=0),symbolSize=1)

    def selectResponse(self):
        responseFile = QFileDialog.getOpenFileName(self, 'Select response curve',)[0]
        # print(responseFile[0])
        self.lineEdit_response.setText(responseFile)

    def plotResponse(self):
        self.widget_response.clear()

        path = self.lineEdit_directory.text()
        sub_str = self.lineEdit_subdirectories.text()
        sub_list = sub_str.split(',')
        folderPathList = [path + '/' + item + '/' for item in sub_list]
        im_all, re_all = readImRePhase(folderPathList, fileNameIm=self.lineEdit_im.text(), fileNameRe=self.lineEdit_re.text(), naiveScale=float(self.lineEdit_unitConversionData.text()))
        self.widget_response.plot(im_all, re_all,pen=pg.mkPen('b', width=1))

        self.cond_array, self.im_sim_raw, self.re_sim_raw = readSimulatedImReCSV(self.lineEdit_response.text(), comsolScale=float(self.lineEdit_unitConversionSimulation.text()))
        self.im_sim = self.im_sim_raw*float(self.lineEdit_xrefactor.text())
        self.re_sim = self.re_sim_raw*float(self.lineEdit_yrefactor.text())
        self.widget_response.plot(self.im_sim, self.re_sim)
        # print(12234)

    def selectLaserScreenshot(self):
        laserScreenshot = QFileDialog.getOpenFileName(self, 'Select Laser Screenshot Image', )[0]
        self.lineEdit_laserScreenshot.setText(laserScreenshot)

    def selectCalibratedPreviewTxt(self):
        calibratedPreviewTXT = QFileDialog.getOpenFileName(self, 'Select .txt Data File')[0]
        self.lineEdit_calibrationFile.setText(calibratedPreviewTXT)

    def plotLaserScreenshot(self):
        self.label_laserScreenshot.pt_edges = None
        self.label_laserScreenshot.center = None
        self.label_center.setText("Center Coordinate:\nPlease click desired center position to get coordinates\nDefault: x = 0, y = 0")
        self.label_laserScreenshot.clear()

        self.xyminmax=np.array([self.lineEdit_xmin.text(),self.lineEdit_xmax.text(),self.lineEdit_ymin.text(),
                                self.lineEdit_ymax.text()]).astype(float)
        xrange = self.xyminmax[1]-self.xyminmax[0]
        yrange = self.xyminmax[3]-self.xyminmax[2]
        height = self.label_laserScreenshot.height()
        width = self.label_laserScreenshot.width()
        self.label_laserScreenshot.setAlignment(Qt.AlignCenter)
        # if xrange/width < yrange/height:
        ratio = np.min([width/xrange,height/yrange])
        self.laserScreenshotWidth, self.laserScreenshotHeight = int(xrange*ratio), int(yrange*ratio)
        self.pixmap_laser = QPixmap(self.lineEdit_laserScreenshot.text()).scaled(self.laserScreenshotWidth,self.laserScreenshotHeight, Qt.IgnoreAspectRatio)

        # print(self.pixmap_laser.size())

        self.label_laserScreenshot.setPixmap(self.pixmap_laser)
        self.label_laserScreenshot.pixmap_laser = self.pixmap_laser



    def plotLaserLinecut(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        laserimg_cropped = np.asarray(Image.open(self.lineEdit_laserScreenshot.text()))
        if len(laserimg_cropped.shape) == 3:
            laserimg_cropped = np.sum(laserimg_cropped, axis = 2)
        # print(laserimg_cropped.shape)
        laser_X_cropped = np.linspace(self.xyminmax[0],self.xyminmax[1],np.shape(laserimg_cropped)[1])
        laser_Y_cropped = np.linspace(self.xyminmax[2],self.xyminmax[3],np.shape(laserimg_cropped)[0])

        # laser_rList, laser_zList, laser_rDict = radialAverageByLinecuts(laserimg_cropped, (0, 0), laser_X_cropped,
        #                                                                 laser_Y_cropped, radialSteps=300,
        #                                                                 threshold=1 / 6 * 1, angleSteps=10)

        if self.label_laserScreenshot.centerCoords == None:
            center = (0,0)
        else:
            center = self.label_laserScreenshot.centerCoords
        laser_rList, laser_zList, pt_edges = radialAverage(laserimg_cropped,center,laser_X_cropped,laser_Y_cropped,
                                                    angleSteps=int(self.lineEdit_angleSteps.text()),
                                                    angleOffsetDegree=float(self.lineEdit_offset.text()))
        # print(laser_X_cropped.min(), laser_X_cropped.max())
        # print(laser_Y_cropped.min(), laser_Y_cropped.max())

        # selectxyarray = np.asarray(radialAverageByLinecuts.selectxy)
        # print(selectxyarray.reshape(-1,2))
        laser_zList_norm = laser_zList / np.max(laser_zList)
        laser_zList_edgesupress = laser_zList_norm#np.asarray(
            # [item / (abs(laser_rList[i]) ** 2 * 0.065 + 1) for i, item in enumerate(laser_zList_norm)])
        dataPointGap = int(self.lineEdit_dataPointGap.text())
        normalizeMin = float(self.lineEdit_normalizeMin.text())
        normalizeMax = float(self.lineEdit_normalizeMax.text())

        laser_zList_edgesupress = (laser_zList_edgesupress - np.min(laser_zList_edgesupress)) / \
                                  (np.max(laser_zList_edgesupress) - np.min(laser_zList_edgesupress)) * \
                                  (normalizeMax - normalizeMin) + normalizeMin
        self.widget_laserFit.plot(laser_rList[::dataPointGap],laser_zList_edgesupress[::dataPointGap],symbol='o',pen=None,symbolPen = pg.mkPen(color=(0, 0, 255)),symbolSize=5)#pen=pg.mkPen('b'))
        # plt.scatter(laser_rList[::4], laser_zList_edgesupress[::4], marker='o', color='blue', s=50, zorder=5, alpha=1,
        #             label='Laser profile')
        self.label_laserScreenshot.pt_edges = pt_edges
        self.label_laserScreenshot.update()#???

        QApplication.restoreOverrideCursor()

    def plotLaserFit(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        xx,yy,z = diffusion_map(1e-100,float(self.lineEdit_laserRadius.text())*np.sqrt(2),point_num=100,pos_max=15)
        x_axis_fit = xx[0]
        total = np.sum(z)
        z /= total
        z_axis_fit = z[round(z.shape[0] / 2)]
        z0 = np.max(z_axis_fit)  # or np.max(z). They are the same
        # plt.plot(x_axis_fit, z_axis_fit / z0, label='L={}μm'.format(int(L)), color='black')
        self.widget_laserFit.plot(x_axis_fit,z_axis_fit/z0,pen=pg.mkPen(width=3))
        QApplication.restoreOverrideCursor()

    def plotCalibrationPreviewRawData(self):
        array = readTXT(self.lineEdit_calibrationFile.text())
        if hasattr(self.widget_calibrationPreviewRaw, "canvas"):
            # ref: https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget
            self.verticalLayout_calibrationPreviewRaw.removeWidget(self.widget_calibrationPreviewRaw.canvas)
            self.widget_calibrationPreviewRaw.canvas.deleteLater()
            self.widget_calibrationPreviewRaw.canvas = None
        self.widget_calibrationPreviewRaw.canvas = FigureCanvas(Figure())
        self.verticalLayout_calibrationPreviewRaw.addWidget(self.widget_calibrationPreviewRaw.canvas)

        self.widget_calibrationPreviewRaw.canvas.axes = self.widget_calibrationPreviewRaw.canvas.figure.add_subplot(111)
        self.widget_calibrationPreviewRaw.canvas.axes.set_aspect(1)
        X = np.linspace(float(self.lineEdit_CalibrationPreview_xmin.text()),
                      float(self.lineEdit_CalibrationPreview_xmax.text()), array.shape[1])
        Y = np.linspace(float(self.lineEdit_CalibrationPreview_ymin.text()),
                      float(self.lineEdit_CalibrationPreview_ymax.text()), array.shape[0])
        self.widget_calibrationPreviewRaw.canvas.axes.pcolormesh(X, Y, array, shading='auto')
        self.widget_calibrationPreviewRaw.canvas.figure.tight_layout(pad = 4)

    def plotCalibrationPreviewCalibrated(self):
        array = readTXT(self.lineEdit_calibrationFile.text())
        if hasattr(self.widget_calibrationPreviewCalibrated, "canvas"):
            self.verticalLayout_calibrationPreviewCalibrated.removeWidget(self.widget_calibrationPreviewCalibrated.canvas)
            self.widget_calibrationPreviewCalibrated.canvas.deleteLater()
            self.widget_calibrationPreviewCalibrated.canvas = None

        self.widget_calibrationPreviewCalibrated.canvas = FigureCanvas(Figure())
        self.verticalLayout_calibrationPreviewCalibrated.addWidget(self.widget_calibrationPreviewCalibrated.canvas)

        self.widget_calibrationPreviewCalibrated.canvas.axes = self.widget_calibrationPreviewCalibrated.canvas.figure.add_subplot(111)
        self.widget_calibrationPreviewCalibrated.canvas.axes.set_aspect(1)
        X = np.linspace(float(self.lineEdit_CalibrationPreview_xmin.text()),
                      float(self.lineEdit_CalibrationPreview_xmax.text()), array.shape[1])
        Y = np.linspace(float(self.lineEdit_CalibrationPreview_ymin.text()),
                      float(self.lineEdit_CalibrationPreview_ymax.text()), array.shape[0])
        X = calibrate_xlist(X, coeff1=float(self.lineEdit_xc1.text()), coeff2=float(self.lineEdit_xc2.text()),
                            extra_scale_x=float(self.lineEdit_xscaling.text()))
        Y = calibrate_ylist(Y, coeff1=float(self.lineEdit_yc1.text()), coeff2=float(self.lineEdit_yc2.text()),
                            extra_scale_y=float(self.lineEdit_yscaling.text()))
        X = X - np.min(X)
        Y = Y - np.min(Y)
        self.widget_calibrationPreviewCalibrated.canvas.axes.pcolormesh(X, Y, array, shading='auto')
        self.widget_calibrationPreviewCalibrated.canvas.figure.tight_layout(pad = 4)

    def calibrateAll(self):
        self.pushButton_calibrateAll.setEnabled(False)
        self.pushButton_calibrateAllStop.setEnabled(True)
        self.progressBar_calibrateAll.setValue(0)
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.lineEdit_calibrateAllFiles.setEnabled(False)
        self.lineEdit_xmin_2.setEnabled(False)
        self.lineEdit_ymin_2.setEnabled(False)
        self.lineEdit_xmax_2.setEnabled(False)
        self.lineEdit_ymax_2.setEnabled(False)
        self.worker.finished.connect(lambda: (
            self.lineEdit_calibrateAllFiles.setEnabled(True),
            self.lineEdit_xmin_2.setEnabled(True),
            self.lineEdit_ymin_2.setEnabled(True),
            self.lineEdit_xmax_2.setEnabled(True),
            self.lineEdit_ymax_2.setEnabled(True),
            self.pushButton_calibrateAll.setEnabled(True),
            self.pushButton_calibrateAllStop.setEnabled(False)
        ))
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        def report(n):
            self.progressBar_calibrateAll.setValue(n)
        self.worker.progress.connect(report)
        self.thread.start()

    def calibrateAllStop(self):
        self.worker.isRunning = False
        self.progressBar_calibrateAll.setValue(0)



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, parent):
        super(Worker, self).__init__()
        self.isRunning = True
        self.parrent = parent
    def run(self):
        # for i in range(5):
        #     sleep(1)
            # print(i)
        path = self.parrent.lineEdit_directory.text()
        sub_str = self.parrent.lineEdit_subdirectories.text()
        sub_list = sub_str.split(',')
        folderPathList = [path + '/' + item + '/' for item in sub_list]
        files = self.parrent.lineEdit_calibrateAllFiles.text().split(',')
        files = [item for item in files if len(item) != 0]
        # self.progressBar_calibrateAll.setValue(1)
        for i, folder in enumerate(folderPathList):
            if not self.isRunning:
                break
            for j, file in enumerate(files):
                if not self.isRunning:
                    break
                array = readTXT(folder + file)
                X = np.linspace(float(self.parrent.lineEdit_xmin_2.text()), float(self.parrent.lineEdit_xmax_2.text()), array.shape[1])
                Y = np.linspace(float(self.parrent.lineEdit_ymin_2.text()), float(self.parrent.lineEdit_ymax_2.text()), array.shape[0])
                X = calibrate_xlist(X, coeff1=float(self.parrent.lineEdit_xc1.text()), coeff2=float(self.parrent.lineEdit_xc2.text()),
                                    extra_scale_x=float(self.parrent.lineEdit_xscaling.text()))

                Y = calibrate_ylist(Y, coeff1=float(self.parrent.lineEdit_yc1.text()), coeff2=float(self.parrent.lineEdit_yc2.text()),
                                    extra_scale_y=float(self.parrent.lineEdit_yscaling.text()))
                X = X - np.min(X)
                Y = Y - np.min(Y)
                X, Y = np.meshgrid(X, Y)
                tmp, _, _ = resample(array, X, Y, float(self.parrent.lineEdit_xmin_2.text()),
                                     float(self.parrent.lineEdit_xmax_2.text()),
                                     float(self.parrent.lineEdit_ymin_2.text()), float(self.parrent.lineEdit_ymax_2.text()), size=None, parent = self)

                if not self.isRunning:
                    break
                print((i * len(files) + j + 1) / len(folderPathList) / len(files) * 100);
                self.progress.emit((i * len(files) + j + 1) / len(folderPathList) / len(files) * 100)
                # self.progressBar_calibrateAll.setValue(
                #     (i * len(files) + j + 1) / len(folderPathList) / len(files) * 100)
                np.savetxt(folder + file[:-4] + "_calibrated.txt", array)
                SaveParkTiff(array, float(self.parrent.lineEdit_xmax_2.text())-float(self.parrent.lineEdit_xmin_2.text()),
                             float(self.parrent.lineEdit_ymax_2.text())-float(self.parrent.lineEdit_ymin_2.text()), folder + file[:-4] + "_calibrated.tiff")

        self.finished.emit()




if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())