
from widgets import widgets
from PyQt4 import QtCore, QtGui


class Widget(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Widget, self).__init__(parent)
        self.config = config

        self.setFixedWidth(100)
        self.setFixedHeight(100)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.red)
        self.setPalette(palette)

        self.show()

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:

            mimeData = QtCore.QMimeData()
            mimeData.setText('%d,%d' % (e.x(), e.y()))

            # show the ghost image while dragging
            pixmap = QtGui.QPixmap.grabWidget(self)
            painter = QtGui.QPainter(pixmap)
            painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
            painter.end()

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.pos())

            drag.exec_(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):
        super(Widget, self).mousePressEvent(e)
