# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import QFile, Qt
# from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap,QImage, QPainter, QPen, QBrush, QPolygon
import pyqtgraph as pg
from utils import readSimulatedImReCSV,readImRePhase,diffusion_map,radialAverageByLinecuts
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
        self.connect()
        self.center = QPolygon()
        self.piximg = None
        # directoryName = None
        # responseFile = None
        self.widget_response.setBackground('w')
        self.widget_laserScreenshot.setBackground('w')
        self.widget_laserFit.setBackground('w')
        self.im_sim_raw = None
        self.re_sim_raw = None
        self.cond_array = None
        self.im_sim = None
        self.re_sim = None
        self.laserScreenshot = None

        # self.graphWidget = pg.PlotWidget()
        # # self.setCentralWidget(self.graphWidget)
        #
        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        #
        # # plot data: x, y values
        # self.graphWidget.plot(hour, temperature)
        # self.widget_response = self.graphWidget


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)


    # def extraConfiguration(self):
    #     self.widget_response.canvas = FigureCanvas(Figure())
    #     # self.widget_response.canvas.resize(2,1)
    #     vertical_layout = QVBoxLayout()
    #     vertical_layout.addWidget(self.widget_response.canvas)
    #
    #
    #
    #     self.widget_response.canvas.axes = self.widget_response.canvas.figure.add_subplot(111)
    #     self.widget_response.canvas.axes.set_xlabel('MIM-Im')
    #     self.widget_response.canvas.axes.set_ylabel('MIM-Re')
    #     # self.widget_response.canvas.figure.tight_layout(pad=5)
    #     # self.widget_response.canvas.axes.set_size(1,2)
    #     self.widget_response.setLayout(vertical_layout)
    #
    #     # self.label_ylabel.rotate(90)


    def connect(self):
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

    def selectDirectory(self):
        directoryName = QFileDialog.getExistingDirectory(self, 'Select directory')#getOpenFileName(self, 'Open file', '.', '')
        self.lineEdit_directory.setText(directoryName)
        # self.image = QImage()
        # self.image.load(filename) # another way to import image

        # pixtmp = QPixmap(directoryName)
        # self.piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        # self.label_image.setPixmap(self.piximg)#QPixmap.fromImage(self.image))


    def findDotPos(self,event):
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        # print(x,y)
        self.center.clear()
        self.center << pos
        self.pos = pos
        self.label_center.setText(str(x)+' ,'+str(y))
        self.update()
        self.label_image.update()

    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     if self.piximg != None:
    #         qp = QPainter(self)
    #         qp.setRenderHints(QPainter.Antialiasing)
    #         pen = QPen(Qt.red,5)
    #         brush = QBrush(Qt.red)
    #         qp.setPen(pen)
    #         qp.setBrush(brush)
    #         qp.drawPixmap(self.label_image.rect(), self.piximg)
    #         qp.drawEllipse(self.label_image.mapToParent(self.center.point(0)),5,5)
    #         print(self.label_image.mapToParent(self.center.point(0)))
    #         print(self.piximg)

    # def combineSubDirectories(self):
    #     print(self.lineEdit_subdirectories.text())

    # def plotScatters(self):

        # self.widget_response.plot(im_all, re_all, pen=None,symbol = 'o',symbolPen = pg.mkPen(color=(0, 0, 255), width=0),symbolSize=1)

    def selectResponse(self):
        responseFile = QFileDialog.getOpenFileName(self, 'Select response curve',)[0]
        # print(responseFile[0])
        self.lineEdit_response.setText(responseFile)

        # pixtmp = QPixmap(responseFile)
        # self.piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        # self.label_response.setPixmap(self.piximg)#QPixmap.fromImage(self.image))

        # self.plotResponse()


    # def updateResponse(self,x,y):
    #     # self.widget_response.canvas.axes.clear()
    #     # self.widget_response.canvas.axes.plot(x,y)
    #     # # self.widget_response.canvas.axes.set_xlabel('MIM-Im')
    #     # # self.widget_response.canvas.axes.set_ylabel('MIM-Re')
    #     # # self.widget_response.canvas.figure.tight_layout(pad=3)
    #     # # self.widget_response.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
    #     # # self.widget_response.canvas.axes.set_title(' Cosinus - Sinus Signal')
    #     #
    #     # self.widget_response.canvas.draw()
    #     self.widget_response.clear()
    #     self.widget_response.plot(x,y)

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
        # pixmap = QPixmap(self.lineEdit_laserScreenshot.text()).scaled(200, 200, Qt.KeepAspectRatio)
        # self.label_laserScreenshot.setPixmap(pixmap)

        # self.plotLaserScreenshot()

        # print(self.lineEdit_laserScreenshot.text())
        # image_array = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(self.lineEdit_laserScreenshot.text()))#np.asarray(Image.open(self.lineEdit_laserScreenshot.text()))
        # print(image_array)
        # self.widget_laserScreenshot.addItem(image_array)

        # self.piximg = pixtmp.scaled(200, 200, Qt.KeepAspectRatio)

    def plotLaserScreenshot(self):
        pixmap = QPixmap(self.lineEdit_laserScreenshot.text()).scaled(200, 200, Qt.KeepAspectRatio)
        print(pixmap)
        self.label_laserScreenshot.setPixmap(pixmap)

    def plotLaserFit(self):
        xx,yy,z = diffusion_map(1e-100,float(self.lineEdit_laserRadius.text())*np.sqrt(2),point_num=100,pos_max=15)
        x_axis_fit = xx[0]
        total = np.sum(z)
        z /= total
        z_axis_fit = z[round(z.shape[0] / 2)]
        z0 = np.max(z_axis_fit)  # or np.max(z). They are the same
        # plt.plot(x_axis_fit, z_axis_fit / z0, label='L={}μm'.format(int(L)), color='black')
        self.widget_laserFit.plot(x_axis_fit,z_axis_fit/z0,pen=pg.mkPen(width=3))

        laserimg_cropped = np.asarray(Image.open(self.lineEdit_laserScreenshot.text()))
        laser_X_cropped = np.linspace(-15,15,np.shape(laserimg_cropped)[1])
        laser_Y_cropped = np.linspace(-15,15,np.shape(laserimg_cropped)[0])

        laser_rList, laser_zList, laser_rDict = radialAverageByLinecuts(laserimg_cropped, (0, 0), laser_X_cropped,
                                                                        laser_Y_cropped, radialSteps=300,
                                                                        threshold=1 / 6 * 1, angleSteps=10)

        selectxyarray = np.asarray(radialAverageByLinecuts.selectxy)
        print(selectxyarray.reshape(-1,2))
        laser_zList_norm = laser_zList / np.max(laser_zList)
        laser_zList_edgesupress = np.asarray(
            [item / (abs(laser_rList[i]) ** 2 * 0.065 + 1) for i, item in enumerate(laser_zList_norm)])
        self.widget_laserFit.plot(laser_rList[::4],laser_zList_edgesupress[::4],symbol='o',pen=None,symbolPen = pg.mkPen(color=(0, 0, 255)),symbolSize=5)#pen=pg.mkPen('b'))
        # plt.scatter(laser_rList[::4], laser_zList_edgesupress[::4], marker='o', color='blue', s=50, zorder=5, alpha=1,
        #             label='Laser profile')


if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
