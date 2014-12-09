import pygal
from pygal.style import Style
from SVGWidget import SVGWidget


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
        super(Gauge, self).setFixedWidth(375)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Gauge()
        
        # styling
        chart.style = self.style
        chart.margin = 20
        chart.label_font_size = self.config.label_font_size
        chart.title_font_size = self.config.title_font_size
        chart.human_readable = True
        chart.show_legend = False
        chart.print_values = False # the value number on top of the needle
        chart.title = self.config.title
        chart.range = [self.config.min, self.config.max]

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)

class Horizontal_Bar(SVGWidget):
    def __init__(self, parent, config):
        super(Horizontal_Bar, self).__init__(parent, config)

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
        super(Horizontal_Bar, self).setFixedWidth(375)
        super(Horizontal_Bar, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Bar()
        
        # styling
        chart.style = self.style
        chart.margin = 20
        chart.label_font_size = self.config.label_font_size
        chart.title_font_size = self.config.title_font_size
        chart.human_readable = True
        chart.show_legend = False
        chart.print_values = False # the value number on top of the needle
        chart.title = self.config.title
        chart.range = [self.config.min, self.config.max]

        value = 0
        if not response.is_null():
            value = response.value

        chart.add(self.command.name, value)

        self.showChart(chart)
