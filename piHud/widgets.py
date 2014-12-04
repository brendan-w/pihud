import pygal
from pygal.style import Style
from SVGWidget import SVGWidget


class Gauge(SVGWidget):
    def __init__(self, parent, command):
        super(Gauge, self).__init__(parent)
        super(Gauge, self).setFixedWidth(350)
        super(Gauge, self).setFixedHeight(400)

        self.command = command
        self.style = Style(
            background='black',
            plot_background='transparent',
            foreground='#53B9E8',
            foreground_light='#53A0E8',
            foreground_dark='transparent',
            colors=('#53B9E8', '#53B9E8'))

    def render(self, response):
        """ function called by python-OBD with new data to be rendered """
        gauge_chart = pygal.Gauge(human_readable=True, width=200, height=250, style=self.style)
        
        gauge_chart.show_legend = False
        gauge_chart.title = self.command.name
        gauge_chart.range = [0, 8000]

        value = 0
        if isinstance(response.value, float):
            value = response.value

        gauge_chart.add(self.command.name, value)

        self.load(gauge_chart.render())
