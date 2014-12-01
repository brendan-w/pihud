from PyQt4 import QtCore, QtGui, QtSvg
import obd
import pygal
from SVGWidget import SVGWidget

class Gauge(SVGWidget):
    def __init__(self, parent, command):
        super(Gauge, self).__init__(parent)
        super(Gauge, self).setFixedWidth(500)
        super(Gauge, self).setFixedHeight(400)

        self.command = command

    def get_command(self):
        return self.command

    def render(self, response):
        gauge_chart = pygal.Gauge(human_readable=True, width=300, height=200)
        gauge_chart.title = self.command.name
        gauge_chart.range = [0, 8000]

        value = 0
        if isinstance(response.value, float):
            value = response.value

        print response.value

        gauge_chart.add(self.command.name, value)
        chart = QtCore.QByteArray(gauge_chart.render())
        super(Gauge, self).load(chart)
