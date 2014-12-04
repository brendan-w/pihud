
from PyQt4 import QtCore, QtGui, QtSvg


class SVGWidget(QtSvg.QSvgWidget):

    def __init__(self, parent):
        super(SVGWidget,self).__init__(parent)

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.RightButton:

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
        super(SVGWidget, self).mousePressEvent(e)

    def load(self, svg):
        """ override the QT load function for ease of handling pygal SVGs """

        # PyQt has a rendering issue with the following CSS
        # delete it by replacing it with empty brackets
        # https://github.com/brendanwhitfield/piHud/issues/2
        svg = svg.replace(" .series{stroke-width:1.0;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:0,0}", " .series{}")

        # wrap in PyQt byteArray
        byteArray = QtCore.QByteArray(svg)
        super(SVGWidget, self).load(byteArray)
