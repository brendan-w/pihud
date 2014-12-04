
from PyQt4 import QtCore, QtGui, QtSvg


class SVGWidget(QtSvg.QSvgWidget):

    def __init__(self, parent, config):
        super(SVGWidget,self).__init__(parent)
        self.config = config
        self.command = config.command

        if config.position is not None:
            self.move(config.position["x"], config.position["y"])
        else:
            self.auto_position()

        if config.dimensions is not None:
            self.setFixedWidth(config.dimensions['x'])
            self.setFixedHeight(config.dimensions['y'])
        else:
            self.auto_dimensions()


    def auto_position(self):
        """ should be overriden by subclass (abstract) """
        self.move(0, 0)


    def auto_dimensions(self):
        """ should be overriden by subclass (abstract) """
        self.setFixedWidth(400)
        self.setFixedHeight(400)


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

        # wrap in PyQt byteArray
        byteArray = QtCore.QByteArray(svg)
        self.load(byteArray)
