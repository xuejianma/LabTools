# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QFile, Qt, QSize
# from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap,QImage, QPainter, QPen, QBrush, QPolygon
import pyqtgraph as pg
from utils import readSimulatedImReCSV,readImRePhase,diffusion_map,radialAverageByLinecuts,radialAverage
from PIL import Image
# import randomQtUiTools
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

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
        self.laserScreenshot = None

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
        self.laserScreenshot = QFileDialog.getOpenFileName(self, 'Select Laser Screenshot Image', )[0]
        self.lineEdit_laserScreenshot.setText(self.laserScreenshot)

    def plotLaserScreenshot(self):
        self.xyminmax=np.array([self.lineEdit_xmin.text(),self.lineEdit_xmax.text(),self.lineEdit_ymin.text(),
                                self.lineEdit_ymax.text()]).astype(float)
        xrange = self.xyminmax[1]-self.xyminmax[0]
        yrange = self.xyminmax[3]-self.xyminmax[2]
        height = self.label_laserScreenshot.height()
        width = self.label_laserScreenshot.width()
        self.label_laserScreenshot.setAlignment(Qt.AlignCenter)
        # if xrange/width < yrange/height:
        ratio = np.min([width/xrange,height/yrange])
        self.laserScreenshotWidth,self.laserScreenshotHeight = int(xrange*ratio), int(yrange*ratio)
        self.pixmap_laser = QPixmap(self.lineEdit_laserScreenshot.text()).scaled(self.laserScreenshotWidth,self.laserScreenshotHeight, Qt.IgnoreAspectRatio)

        # print(self.pixmap_laser.size())

        self.label_laserScreenshot.setPixmap(self.pixmap_laser)
        self.label_laserScreenshot.pixmap_laser = self.pixmap_laser



    def plotLaserLinecut(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        laserimg_cropped = np.asarray(Image.open(self.lineEdit_laserScreenshot.text()))
        laser_X_cropped = np.linspace(self.xyminmax[0],self.xyminmax[1],np.shape(laserimg_cropped)[1])
        laser_Y_cropped = np.linspace(self.xyminmax[2],self.xyminmax[3],np.shape(laserimg_cropped)[0])

        # laser_rList, laser_zList, laser_rDict = radialAverageByLinecuts(laserimg_cropped, (0, 0), laser_X_cropped,
        #                                                                 laser_Y_cropped, radialSteps=300,
        #                                                                 threshold=1 / 6 * 1, angleSteps=10)

        if self.label_laserScreenshot.centerCoords == None:
            center = (0,0)
        else:
            center = self.label_laserScreenshot.centerCoords
        laser_rList, laser_zList, _ = radialAverage(laserimg_cropped,center,laser_X_cropped,laser_Y_cropped,
                                                    angleSteps=int(self.lineEdit_angleSteps.text()),
                                                    angleOffsetDegree=int(self.lineEdit_offset.text()))
        print(laser_X_cropped.min(), laser_X_cropped.max())
        print(laser_Y_cropped.min(), laser_Y_cropped.max())

        # selectxyarray = np.asarray(radialAverageByLinecuts.selectxy)
        # print(selectxyarray.reshape(-1,2))
        laser_zList_norm = laser_zList / np.max(laser_zList)
        laser_zList_edgesupress = laser_zList_norm#np.asarray(
            # [item / (abs(laser_rList[i]) ** 2 * 0.065 + 1) for i, item in enumerate(laser_zList_norm)])
        self.widget_laserFit.plot(laser_rList[::4],laser_zList_edgesupress[::4],symbol='o',pen=None,symbolPen = pg.mkPen(color=(0, 0, 255)),symbolSize=5)#pen=pg.mkPen('b'))
        # plt.scatter(laser_rList[::4], laser_zList_edgesupress[::4], marker='o', color='blue', s=50, zorder=5, alpha=1,
        #             label='Laser profile')

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

if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
