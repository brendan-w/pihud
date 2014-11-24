from PyQt4 import QtCore, QtGui, QtSvg
import pygal


class SVGWidget(QtSvg.QSvgWidget):

    def __init__(self, parent, byteArray):
        super(SVGWidget,self).__init__(parent)
        super(SVGWidget,self).load(byteArray)

    def mouseMoveEvent(self, e):

        if e.buttons() == QtCore.Qt.RightButton:
            drag = QtGui.QDrag(self)
            drag.setMimeData(QtCore.QMimeData())
            drag.setHotSpot(e.pos() - self.rect().topLeft())

            dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):

        super(SVGWidget, self).mousePressEvent(e)


class Example(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.draggables = []

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        bar_chart = pygal.Bar(width= 300 ,height = 200)
        bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
        chart = QtCore.QByteArray(bar_chart.render())

        svg1 = SVGWidget(self, chart)
        self.draggables.append(svg1)

    def dragEnterEvent(self, e):

        e.accept()

    def dropEvent(self, e):

        position = e.pos()
        e.source().move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
