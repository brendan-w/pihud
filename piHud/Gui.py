
from PyQt4 import QtCore, QtGui

class Gui(QtGui.QWidget):
    def __init__(self, parent, connection, config_file):
        super(Gui, self).__init__(parent)
        self.button = QtGui.QPushButton(self)