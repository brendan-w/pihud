
from PyQt4 import QtCore, QtGui, QtSvg


class SVGWidget(QtSvg.QSvgWidget):

    def __init__(self, parent):
        super(SVGWidget,self).__init__(parent)

    def mouseMoveEvent(self, e):

        if e.buttons() == QtCore.Qt.RightButton:
            drag = QtGui.QDrag(self)
            drag.setMimeData(QtCore.QMimeData())
            drag.setHotSpot(e.pos() - self.rect().topLeft())

            dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):

        super(SVGWidget, self).mousePressEvent(e)