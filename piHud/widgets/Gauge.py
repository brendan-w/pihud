
from PyQt4 import QtCore, QtGui


class Gauge(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent)


    def sizeHint(self):
        return QtCore.QSize(360, 400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass