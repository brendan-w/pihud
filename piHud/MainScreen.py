
import obd
from widgets import *
from PyQt4 import QtCore, QtGui


class MainScreen(QtGui.QWidget):

    def __init__(self, parent, connection):
        super(MainScreen, self).__init__(parent)
        self.draggables = []
        self.initUI()

        self.connection = connection

        self.timer = QtCore.QBasicTimer()
        self.timer.start(1000/30, self)

        self.makeChart(obd.commands.RPM)


    def initUI(self):
        self.setAcceptDrops(True)

    def makeChart(self, command):
        self.connection.watch(command)
        self.draggables.append(Gauge(self, command))

    def timerEvent(self, event):
        """ main event loop """
        for w in self.draggables:
            r = self.connection.query(w.get_command())
            w.render(r)


    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        e.source().move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
