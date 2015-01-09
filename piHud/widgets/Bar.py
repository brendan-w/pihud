
from PyQt4 import QtCore, QtGui



class Bar_h(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent)
        self.color = QtGui.QColor(config.color)


    def sizeHint(self):
        return QtCore.QSize(400, 100)


    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(self.rect(), self.color)
        painter.end()

    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Bar_v(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Bar_v, self).__init__(parent)


    def sizeHint(self):
        return QtCore.QSize(180, 400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass
