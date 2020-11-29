# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import QFile, Qt
# from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap,QImage, QPainter, QPen, QBrush, QPolygon
import pyqtgraph as pg
from utils import readSimulatedImReCSV,readImRePhase
import random
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
        self.directoryName = None
        self.responseFile = None
        self.Widget_response.setBackground('w')
        self.im_sim_raw = None
        self.re_sim_raw = None
        self.cond_array = None
        self.im_sim = None
        self.re_sim = None

        # self.graphWidget = pg.PlotWidget()
        # # self.setCentralWidget(self.graphWidget)
        #
        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        #
        # # plot data: x, y values
        # self.graphWidget.plot(hour, temperature)
        # self.Widget_response = self.graphWidget


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)


    # def extraConfiguration(self):
    #     self.Widget_response.canvas = FigureCanvas(Figure())
    #     # self.Widget_response.canvas.resize(2,1)
    #     vertical_layout = QVBoxLayout()
    #     vertical_layout.addWidget(self.Widget_response.canvas)
    #
    #
    #
    #     self.Widget_response.canvas.axes = self.Widget_response.canvas.figure.add_subplot(111)
    #     self.Widget_response.canvas.axes.set_xlabel('MIM-Im')
    #     self.Widget_response.canvas.axes.set_ylabel('MIM-Re')
    #     # self.Widget_response.canvas.figure.tight_layout(pad=5)
    #     # self.Widget_response.canvas.axes.set_size(1,2)
    #     self.Widget_response.setLayout(vertical_layout)
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

    def selectDirectory(self):
        self.directoryName = QFileDialog.getExistingDirectory(self, 'Select directory')#getOpenFileName(self, 'Open file', '.', '')
        self.lineEdit_directory.setText(self.directoryName)
        # self.image = QImage()
        # self.image.load(filename) # another way to import image

        # pixtmp = QPixmap(self.directoryName)
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

        # self.Widget_response.plot(im_all, re_all, pen=None,symbol = 'o',symbolPen = pg.mkPen(color=(0, 0, 255), width=0),symbolSize=1)

    def selectResponse(self):
        self.responseFile = QFileDialog.getOpenFileName(self, 'Select response curve',)[0]
        # print(self.responseFile[0])
        self.lineEdit_response.setText(self.responseFile)

        # pixtmp = QPixmap(self.responseFile)
        # self.piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        # self.label_response.setPixmap(self.piximg)#QPixmap.fromImage(self.image))


        self.plotResponse()

    # def updateResponse(self,x,y):
    #     # self.Widget_response.canvas.axes.clear()
    #     # self.Widget_response.canvas.axes.plot(x,y)
    #     # # self.Widget_response.canvas.axes.set_xlabel('MIM-Im')
    #     # # self.Widget_response.canvas.axes.set_ylabel('MIM-Re')
    #     # # self.Widget_response.canvas.figure.tight_layout(pad=3)
    #     # # self.Widget_response.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
    #     # # self.Widget_response.canvas.axes.set_title(' Cosinus - Sinus Signal')
    #     #
    #     # self.Widget_response.canvas.draw()
    #     self.Widget_response.clear()
    #     self.Widget_response.plot(x,y)

    def plotResponse(self):
        self.Widget_response.clear()

        path = self.lineEdit_directory.text()
        sub_str = self.lineEdit_subdirectories.text()
        sub_list = sub_str.split(',')
        folderPathList = [path + '/' + item + '/' for item in sub_list]
        im_all, re_all = readImRePhase(folderPathList, fileNameIm=self.lineEdit_im.text(), fileNameRe=self.lineEdit_re.text(), naiveScale=float(self.lineEdit_unitConversionData.text()))
        self.Widget_response.plot(im_all, re_all,pen=pg.mkPen('b', width=1))

        self.cond_array, self.im_sim_raw, self.re_sim_raw = readSimulatedImReCSV(self.lineEdit_response.text(), comsolScale=float(self.lineEdit_unitConversionSimulation.text()))
        self.im_sim = self.im_sim_raw*float(self.lineEdit_xrefactor.text())
        self.re_sim = self.re_sim_raw*float(self.lineEdit_yrefactor.text())
        self.Widget_response.plot(self.im_sim, self.re_sim)
        print(12234)




if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
