
from PyQt4 import QtCore, QtGui


class Graph(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Graph, self).__init__(parent)

        # initialize an empty buffer 
        self.buffer = [0] * config.buffer_size


    def sizeHint(self):
        return QtCore.QSize(400, 300)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass


