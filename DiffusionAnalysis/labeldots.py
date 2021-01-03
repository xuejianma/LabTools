from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter,QPen,QBrush,QPolygon
from PyQt5.QtCore import Qt

class LabelDots(QLabel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.center = QPolygon()
        self.pixmap_laser = None
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        # self.label_laserScreenshot.clear()
        # self.clear()
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        Parent = self.parent().parent().parent().parent()
        Width, Height = self.width(),self.height()
        width, height = Parent.laserScreenshotWidth, Parent.laserScreenshotHeight
        widthDiff,heightDiff = Width-width, Height-height
        xmin,xmax,ymin,ymax = Parent.xyminmax
        xcoord,ycoord = (x-widthDiff/2)/width*(xmax-xmin)+xmin,(Height-y-heightDiff/2)/height*(ymax-ymin)+ymin
        print(xcoord,ycoord)
        self.center.clear()
        self.center << pos
        # print(pos,9999999,self.center)
        self.pos = pos
        # self.label_center.setText(str(x) + ' , ' + str(y))
        # print(x, y, 111)
        # print(self.center.point(0), 222)
        self.update()
    def paintEvent(self, event):
        super().paintEvent(event)
        # print('tttt')
        if self.pixmap_laser != None:
            # self.abel_laserScreenshotl.clear()
            qp = QPainter(self)
            qp.begin(self)
            qp.setRenderHints(QPainter.Antialiasing,True)
            pen = QPen(Qt.red,5)
            brush = QBrush(Qt.red)
            qp.setPen(pen)
            qp.setBrush(brush)
            # qp.drawPixmap(event.rect(), self.pixmap_laser)
            # self.setPixmap(self.pixmap_laser)
            qp.drawEllipse(self.center.point(0),1,1)
            qp.end()
            # print(self.label_laserScreenshot.mapToParent(self.center.point(0)))
            # print(event.rect())




# def findDotPos(self ,event):
#     self.label_laserScreenshot.clear()
#     pos = event.pos()
#     x = pos.x()
#     y = pos.y()
#     # print(x,y)
#     self.center.clear()
#     # self.label_laserScreenshot.clear()
#     self.center << pos
#     self.pos = pos
#     self.label_center.setText(str(x ) +' , ' +str(y))
#     # self.update()
#     # self.label_image.update()
#     print(x ,y ,111)
#     # self.label_laserScreenshot.clear()
#     # painter = QPainter(self)
#     # pen = QPen()
#     # brush = QBrush(Qt.red)
#     # painter.setPen(pen)
#     # painter.setBrush(brush)
#     # painter.setRenderHint(QPainter.Antialiasing,True)
#     # painter.drawPixmap(self.label_laserScreenshot.rect(),self.pixmap_laser)
#     # painter.drawEllipse(self.label_image.mapToParent(self.center.point(0)), 100, 100)
#     # painter.drawPoint(x,y)
#     # self.label_laserScreenshot.setPixmap(self.pixmap_laser)
#     print(self.center.point(0) ,222)

# def paintEvent2(self, event):
#     super().paintEvent(event)
#     print('tttt')
#     if True:#self.pixmap_laser != None:
#         # self.label_laserScreenshot.clear()
#         qp = QPainter(self)
#         qp.begin(self)
#         qp.setRenderHints(QPainter.Antialiasing,True)
#         pen = QPen(Qt.red,5)
#         brush = QBrush(Qt.red)
#         qp.setPen(pen)
#         qp.setBrush(brush)
#         qp.drawPixmap(event.rect(), self.pixmap_laser)
#         qp.drawEllipse(self.center.point(0),5,5)
#         qp.end()
#         print(self.label_laserScreenshot.mapToParent(self.center.point(0)))
#         print(event.rect())