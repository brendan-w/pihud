
from BaseWidget import BaseWidget
from PyQt4 import QtGui


class Text(BaseWidget):
    def __init__(self, parent, config):
        super(Text, self).__init__(parent, config)

        self.label = QtGui.QLabel(self)
        self.label.setText("Label")

        css = """
            font-size: %ipx;
            color: %s;
        """ % (config.label_font_size, config.color)

        self.label.setStyleSheet(css)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Text, self).setFixedWidth(200)
        super(Text, self).setFixedHeight(75)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """

        value = 0
        if not response.is_null():
            value = response.value

        self.label.setText(str(value) + " " + str(response.unit))
