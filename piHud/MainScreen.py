
import obd
from widgets import *
from PyQt4 import QtCore, QtGui


class MainScreen(QtGui.QWidget):

    def __init__(self, parent, connection):
        super(MainScreen, self).__init__(parent)
        self.draggables = []
        self.setAcceptDrops(True)
        self.connection = connection

        # make test chart
        self.makeChart(obd.commands.RPM)


    def makeChart(self, command):
        chart = Gauge(self, command)
        self.connection.watch(command, chart.render)
        chart.render(self.connection.query(command))
        self.draggables.append(chart)


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        position = e.pos()
        e.source().move(position)
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
