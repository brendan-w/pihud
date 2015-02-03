
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from math import log10
from util import map_value


class Gauge(QWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent)
        self.config = config

        self.color = QColor(config.color)
        self.pen   = QPen(self.color)
        self.brush = QBrush(self.color)
        self.pen.setWidth(2)

        # choose a smart scale step
        scale_len      = config.max - config.min
        self.scale_len = scale_len
        scale_order    = round(log10(scale_len))
        scale_step     = 10 ** (scale_order - 1)        
        
        #                       [      Widget Units     ] [Angle]
        angle_step  = map_value(scale_step, config.min, config.max, 0, 270)
        scale_ticks = int(scale_len // scale_step)
        end_tick    = bool(scale_len % scale_step)

        # assemble a list of angle offsets
        self.scale = [angle_step] * scale_ticks
        if end_tick:
            self.scale += [270 - (angle_step * scale_ticks)]
        self.scale += [0]


    def sizeHint(self):
        return QSize(300, 300)


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)
        
        self.draw_marks(painter)
        self.draw_needle(painter, 1000)

        painter.end()


    def draw_marks(self, painter):
        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(90 + 45)

        x_start = (self.width() / 20) * 9
        x_end   = self.width() / 2

        for a in self.scale:
            painter.drawLine(x_start, 0, x_end, 0)
            painter.rotate(a)

        painter.restore()


    def draw_needle(self, painter, value):
        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)
        angle = map_value(value, self.config.min, self.config.max, 0, 270)
        angle -= 90 + 45
        painter.rotate(angle)

        painter.setBrush(self.brush)

        painter.drawEllipse(QPoint(0,0), 5, 5)

        painter.drawPolygon(
            QPolygon([
                QPoint(-5, 0),
                QPoint(0,   -(self.width() / 20) * 8),
                QPoint(5,  0),
                QPoint(-5, 0)
            ])
        )

        painter.restore()
