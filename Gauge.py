from PyQt4 import QtCore, QtGui, QtSvg
import pygal
import obd
from layout import SVGWidget

class GaugeGraph(SVGWidget):
    def __init__(self, parent, command):
        super(GaugeGraph,self).__init__(parent)
        self.command = command

    def getCommand(self):
        return self.command

    def render(self, response)
        gauge_chart = pygal.Gauge(human_readable = True)
        gauge_chart.title(self.command.name)
        gauge_chart.range = [0,8000]
        gauge_char.add(self.command.name, response.value)
        chart = QTCore.QByteArray(gauge_chart.render())
        super(GaugeGraph,self).load(chart)

