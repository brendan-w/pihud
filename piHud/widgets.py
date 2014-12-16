import pygal
from pygal.style import Style
from SVGWidget import SVGWidget
from PyQt4 import QtCore, QtGui
from util import map_value


class Gauge(SVGWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent, config)

        self.style = Style(
            stroke_width=3.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Gauge, self).setFixedWidth(360)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Gauge()
        
        # styling
        chart.style = self.style
        chart.margin = 20
        chart.print_values = False # the value number on top of the needle

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)



class Bar_v(SVGWidget):
    def __init__(self, parent, config):
        super(Bar_v, self).__init__(parent, config)

        self.style = Style(
            stroke_width=1.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_v, self).setFixedWidth(180)
        super(Bar_v, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Bar()
        
        # styling
        chart.style = self.style

        chart.spacing = 0
        chart.margin  = 0

        chart.print_values = False # the value number on top of the needle

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)



class Bar_h(SVGWidget):
    def __init__(self, parent, config):
        super(Bar_h, self).__init__(parent, config)

        # this should really be done with the QPainter, but I have a deadline, and no time to learn

        self.border_size = 2

        self.bar_x = 0
        self.bar_y = config.label_font_size
        self.bar_width = self.width() - (self.border_size * 2)
        self.bar_height = (self.height() - config.label_font_size) - (self.border_size * 2)

        # create a widget for the background, and make it the same size as the parent
        self.background = QtGui.QWidget(self)
        self.background.setStyleSheet("background-color: %s;" % config.color)
        self.background.setFixedWidth(self.width())
        self.background.setFixedHeight(self.height() - self.bar_y)
        self.background.move(self.bar_x, self.bar_y)

        # make the redline
        if config.redline is not None:
            self.redline = QtGui.QWidget(self)
            self.redline.setStyleSheet("background-color: red;")
            
            offset = map_value(config.redline, self.config.min, self.config.max, 0, self.bar_width)
            self.redline.setFixedWidth(self.bar_width - offset + self.border_size)
            
            self.redline.setFixedHeight(self.height() - self.bar_y)
            self.redline.move(offset + self.border_size, self.bar_y)

        # the bar is made by setting the size of a black cover over the background color
        self.cover = QtGui.QWidget(self)
        self.cover.setStyleSheet("background-color: black;")
        self.cover.setFixedHeight(self.bar_height)

        # make a label for it
        self.label = QtGui.QLabel(self)
        self.label.setText(config.title)
        self.label.move(0, 0)

        css = """
            font-size: %ipx;
            color: %s;
        """ % (config.label_font_size, config.color)

        self.label.setStyleSheet(css)


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Bar_h, self).setFixedWidth(400)
        super(Bar_h, self).setFixedHeight(100)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """

        value = 0
        if not response.is_null():
            value = response.value

            if value > self.config.max:
                value = self.config.max
            elif value < self.config.min:
                value = self.config.min

            
        value = map_value(value, self.config.min, self.config.max, 0, self.bar_width)

        self.cover.move(value + self.border_size, self.bar_y + self.border_size)
        self.cover.setFixedWidth(self.bar_width - value)



class Graph(SVGWidget):
    def __init__(self, parent, config):
        super(Graph, self).__init__(parent, config)

        # initialize an empty buffer 
        self.buffer = [0] * config.buffer_size

        self.style = Style(
            stroke_width=3.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color,))


    def default_dimensions(self):
        """ override default size, called by superclass """
        super(Graph, self).setFixedWidth(400)
        super(Graph, self).setFixedHeight(300)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """

        chart = pygal.Line()
        
        # styling
        chart.style     = self.style
        chart.show_dots = False

        value = 0
        if not response.is_null():
            value = response.value

        # add the new data to the buffer
        self.buffer = [value] + self.buffer[:-1]

        chart.add(self.command.name, self.buffer)

        self.showChart(chart)



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
