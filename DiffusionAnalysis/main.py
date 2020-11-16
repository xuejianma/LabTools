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

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)

    def connect(self):
        self.pushButton_selectImageFile.clicked.connect(self.clicked_selectImageFile)
        self.label_image.mousePressEvent = self.findDotPos

    def clicked_selectImageFile(self):
        filename, filter = QFileDialog.getOpenFileName(self, 'Open file', '.', '')
        self.label_filename.setText(filename)
        # self.image = QImage()
        # self.image.load(filename) # another way to import image
        pixtmp = QPixmap(filename)
        piximg = pixtmp.scaled(200,200,Qt.KeepAspectRatio)
        self.label_image.setPixmap(piximg)#QPixmap.fromImage(self.image))


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
        qp = QPainter(self)
        qp.setRenderHints(QPainter.Antialiasing)
        pen = QPen(Qt.red,5)
        brush = QBrush(Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawEllipse(self.label_image.mapToParent(self.center.point(0)),5,5)
        # qp.raise()
        print(self.label_image.mapToParent(self.center.point(0)))



if __name__ == "__main__":
    app = QApplication([])
    widget = gui()
    widget.show()
    sys.exit(app.exec_())
