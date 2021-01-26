from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter,QPen,QBrush,QPolygon
from PyQt5.QtCore import Qt, QPoint

class LabelDots(QLabel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.center = None
        self.pixmap_laser = None
        self.centerCoords = None
        self.pt_edges = None

    def getCoord(self, x, y):
        Parent = self.parent().parent().parent().parent()
        Width, Height = self.width(), self.height()
        width, height = Parent.laserScreenshotWidth, Parent.laserScreenshotHeight
        widthDiff, heightDiff = Width - width, Height - height
        xmin, xmax, ymin, ymax = Parent.xyminmax
        xcoord, ycoord = (x - widthDiff / 2) / width * (xmax - xmin) + xmin, (Height - y - heightDiff / 2) / height * (
                    ymax - ymin) + ymin
        return xcoord, ycoord
    def getPos(self, xcoord, ycoord):
        Parent = self.parent().parent().parent().parent()
        Width, Height = self.width(), self.height()
        width, height = Parent.laserScreenshotWidth, Parent.laserScreenshotHeight
        widthDiff, heightDiff = Width - width, Height - height
        xmin, xmax, ymin, ymax = Parent.xyminmax
        x = int((xcoord - xmin) / (xmax - xmin) * width + widthDiff / 2)
        y = int(-((ycoord - ymin) / (ymax - ymin) * height + heightDiff / 2 - Height))
        return x, y

    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        # self.label_laserScreenshot.clear()
        # self.clear()
        pos = event.pos()

        x = pos.x()
        y = pos.y()
        xcoord,ycoord = self.getCoord(x, y)
        # print(xcoord,ycoord)
        self.centerCoords = (xcoord,ycoord)
        self.center.clear()
        self.center << pos
        # print(pos,9999999,self.center)
        self.pos = pos
        Parent = self.parent().parent().parent().parent()
        Parent.label_center.setText("Center Coordinate:\nx = "+str(xcoord) + "\ny = " + str(ycoord))
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
            # print(self.center.point(0))
            if self.center == None:
                Parent = self.parent().parent().parent().parent()
                width, height = Parent.laserScreenshotWidth, Parent.laserScreenshotHeight
                self.center = QPolygon()
                self.center << QPoint(*self.getPos(0,0))
            qp.drawEllipse(self.center.point(0),1,1)
            if self.pt_edges != None:
                pen = QPen(Qt.gray, 1)
                brush = QBrush(Qt.gray)
                qp.setPen(pen)
                qp.setBrush(brush)
                # print(self.pt_edges)
                # qp.drawLine(0,0,200,200);
                for pt in self.pt_edges:
                    # print(*pt,123)
                    pt1 = self.getPos(*pt[0])
                    pt2 = self.getPos(*pt[1])
                    qp.drawLine(*pt1, *pt2);
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