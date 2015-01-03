
from SVGWidget import SVGWidget
from PyQt4 import QtCore, QtGui
from util import map_value


class Gauge(SVGWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Gauge, self).setFixedWidth(360)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Bar_v(SVGWidget):
    def __init__(self, parent, config):
        super(Bar_v, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_v, self).setFixedWidth(180)
        super(Bar_v, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Bar_h(SVGWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent, config)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_h, self).setFixedWidth(400)
        super(Bar_h, self).setFixedHeight(100)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Graph(SVGWidget):
    def __init__(self, parent, config):
        super(Graph, self).__init__(parent, config)

        # initialize an empty buffer 
        self.buffer = [0] * config.buffer_size


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Graph, self).setFixedWidth(400)
        super(Graph, self).setFixedHeight(300)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        pass



class Text(SVGWidget):
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
