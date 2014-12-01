from PyQt4 import QtCore, QtGui, QtSvg
import pygal
import obd
from SVGWidget import SVGWidget

class GaugeGraph(SVGWidget):
    def __init__(self, parent, command):
        super(GaugeGraph, self).__init__(parent)
        self.command = command

    def get_command(self):
        return self.command

    def render(self, response):
        gauge_chart = pygal.Gauge(human_readable=True, width=300, height=200)
        gauge_chart.title = self.command.name
        gauge_chart.range = [0, 8000]

        value = 0
        if isinstance(response.value, int):
            value = response.value

        value = 30

        gauge_chart.add(self.command.name, value)
        chart = QtCore.QByteArray(gauge_chart.render())
        super(GaugeGraph,self).load(chart)
