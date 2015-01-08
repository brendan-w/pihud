
from PyQt4 import QtCore, QtGui


class Text(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Text, self).__init__(parent)

        self.label = QtGui.QLabel(self)
        self.label.setText("Label")

        css = """
            font-size: %ipx;
            color: %s;
        """ % (config.label_font_size, config.color)

        self.label.setStyleSheet(css)


    def sizeHint(self):
        return QtCore.QSize(200, 75)        


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """

        value = 0
        if not response.is_null():
            value = response.value

        self.label.setText(str(value) + " " + str(response.unit))
