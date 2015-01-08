
from PyQt4 import QtCore, QtGui


class Bar_v(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Bar_v, self).__init__(parent)


    def sizeHint(self):
        return QtCore.QSize(180, 400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Bar_h(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent)


    def sizeHint(self):
        return QtCore.QSize(400, 100)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass