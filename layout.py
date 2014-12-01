
from PyQt4 import QtCore, QtGui
import obd

from widgets import Gauge



class Layout(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Layout, self).__init__(parent)
        self.draggables = []
        self.initUI()

        obd.debug.console = True
        self.connection = obd.Async()

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
