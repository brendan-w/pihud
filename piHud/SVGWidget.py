
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

    def showChart(self, chart):
        """ handles loading of pygal SVGs """

        # PyQt has a rendering issue with the following CSS
        # https://github.com/brendanwhitfield/piHud/issues/2
        chart.style.stroke_dasharray = ""

        # they have a 'no_prefix' setting, but PyQt couldn't render the result,
        # so the ID is set to be as short as possible (to save memory)
        chart.uuid = ""

        svg = chart.render()

        # for debug
        # text_file = open("output.svg", "w")
        # text_file.write(svg)
        # text_file.close()

        # wrap in PyQt byteArray
        byteArray = QtCore.QByteArray(svg)
        self.load(byteArray)
