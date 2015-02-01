
from PyQt4 import QtCore, QtGui
from math import log10
from util import map_value


class Gauge(QtGui.QWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent)
        self.color = QtGui.QColor(config.color)
        self.pen   = QtGui.QPen(self.color)
        self.pen.setWidth(2)

        # choose a smart scale step
        scale_len   = config.max - config.min
        scale_order = round(log10(scale_len))
        scale_step  = 10 ** (scale_order - 1)        
        
        #                       [      Widget Units     ] [Angle]
        angle_step  = map_value(scale_step, 0, scale_len, 0, 270)
        scale_ticks = int(scale_len // scale_step)
        end_tick    = bool(scale_len % scale_step)

        # assemble a list of angle offsets
        self.scale = [angle_step] * scale_ticks
        if end_tick:
            self.scale += [270 - (angle_step * scale_ticks)]
        self.scale += [0]


    def sizeHint(self):
        return QtCore.QSize(300, 300)


    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.draw_marks(painter)

        painter.end()


    def draw_marks(self, painter):
        painter.save()

        painter.setPen(self.pen)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(90 + 45)

        x_start = (self.width() / 20) * 9
        x_end   = self.width() / 2

        for a in self.scale:
            painter.drawLine(x_start, 0, x_end, 0)
            painter.rotate(a)

        painter.restore()
