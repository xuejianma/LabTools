# """
# Created by Xuejian Ma at 6/18/2020.
# All rights reserved.
# """
# from readConductivities import im_img_all,re_img_all,conductivity_all
# import matplotlib.pyplot as plt
# plt.figure(figsize=(30,20))
# plt.imshow(conductivity_all[-1])
# plt.colorbar()
# # plt.show()
# plt.savefig("C:\Work\Xuejian Ma\Perovskite\imgs/test.png")

from PyQt5 import QtWidgets, QtGui, QtCore


class ImageScroller(QtWidgets.QWidget):
    def __init__(self):
        self.chosen_points = []
        QtWidgets.QWidget.__init__(self)
        self._image = QtGui.QPixmap("image.png")

    def paintEvent2(self, paint_event):
        super().paintEvent(paint_event)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._image)
        pen = QtGui.QPen()
        pen.setWidth(20)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.drawPoint(300, 300)
        painter.drawLine(100, 100, 400, 400)
        print(123123)
        for pos in self.chosen_points:
            painter.drawPoint(pos)

    def mouseReleaseEvent(self, cursor_event):
        self.chosen_points.append(cursor_event.pos())
        # self.chosen_points.append(self.mapFromGlobal(QtGui.QCursor.pos()))
        self.update()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = ImageScroller()
    w.paintEvent = w.paintEvent2
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())