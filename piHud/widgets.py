import pygal
from pygal.style import Style
from SVGWidget import SVGWidget


class Gauge(SVGWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent, config)

        self.style = Style(
            stroke_width=2.0,
            background='transparent',
            plot_background='transparent',
            foreground=config.color,
            foreground_light=config.color,
            foreground_dark='transparent',
            colors=(config.color, config.color))


    def auto_dimensions(self):
        """ override default size """
        super(Gauge, self).setFixedWidth(400)
        super(Gauge, self).setFixedHeight(400)


    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        
        chart = pygal.Gauge(width=200, height=300)
        
        # styling
        chart.style = self.style
        chart.human_readable = True
        chart.show_legend = False
        chart.title = self.command.name
        chart.range = [self.config.min, self.config.max]

        value = 0
        if isinstance(response.value, float):
            value = response.value

        value = 30

        chart.add(self.command.name, value)

        self.showChart(chart)
