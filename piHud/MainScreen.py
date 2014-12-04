
import obd
from widgets import *
from PyQt4 import QtCore, QtGui


class MainScreen(QtGui.QWidget):

    def __init__(self, parent, connection):
        super(MainScreen, self).__init__(parent)

        self.draggables = []
        self.connection = connection

        self.setAcceptDrops(True)

        # make test widget
        self.makeChart(obd.commands.RPM)


    def makeChart(self, command):
        widget = Gauge(self, command)
        self.connection.watch(command, widget.render)
        widget.render(self.connection.query(command)) # testing purposes only
        self.draggables.append(widget)


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):

        # get relative position of mouse from mimedata
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))

        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
