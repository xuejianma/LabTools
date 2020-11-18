# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGridLayout, QLabel
from PyQt5.QtCore import QFile, Qt
# from PyQt5.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap,QImage, QPainter, QPen, QBrush, QPolygon

class gui(QWidget):
    def __init__(self):
        super(gui, self).__init__()
        self.load_ui()
        self.connect()
        self.center = QPolygon()
        self.piximg = None


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)

    def connect(self):
        self.pushButton_directory.clicked.connect(self.selectDirectory)
        self.label_image.mousePressEvent = self.findDotPos
        self.pushButton_tmp.clicked.connect(self.combineSubDirectories)

    def selectDirectory(self):
        directoryName = QFileDialog.getExistingDirectory(self, 'Select directory')#getOpenFileName(self, 'Open file', '.', '')
        self.lineEdit_directory.setText(directoryName)
        # self.image = QImage()
        # self.image.load(filename) # another way to import image

        pixtmp = QPixmap(directoryName)
        self.piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        self.label_image.setPixmap(self.piximg)#QPixmap.fromImage(self.image))


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

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.piximg != None:
            qp = QPainter(self)
            qp.setRenderHints(QPainter.Antialiasing)
            pen = QPen(Qt.red,5)
            brush = QBrush(Qt.red)
            qp.setPen(pen)
            qp.setBrush(brush)
            qp.drawPixmap(self.label_image.rect(), self.piximg)
            qp.drawEllipse(self.label_image.mapToParent(self.center.point(0)),5,5)
            print(self.label_image.mapToParent(self.center.point(0)))
            print(self.piximg)

    def combineSubDirectories(self):
        print(self.lineEdit_subdirectories.text())


if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
