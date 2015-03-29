
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from math import log10
from util import scale, map_scale, map_value, scale_offsets


class Gauge(QWidget):
    def __init__(self, parent, config):
        super(Gauge, self).__init__(parent)

        self.config = config
        self.value = self.config.min

        self.font  = QFont()
        self.color = QColor(config.color)
        self.brush = QBrush(self.color)
        self.pen   = QPen(self.color)

        self.font.setPixelSize(self.config.title_font_size)
        self.pen.setWidth(3)

        self.scale = scale(config.min, config.max)
        self.abs_angles = map_scale(self.scale, 0, 270)
        self.offset_angles = scale_offsets(self.abs_angles)


    def render(self, v):
        # approach the value
        self.value += (v - self.value) / 4
        self.update()


    def sizeHint(self):
        return QSize(300, 300)


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)
        
        self.draw_marks(painter)
        self.draw_needle(painter, self.value)
        self.draw_title(painter, self.config.title)

        painter.end()


    def draw_marks(self, painter):
        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(90 + 45)

        x_start = self.width() / 2
        x_end   = x_start - (self.width() / 20)

        for a in self.offset_angles:
            painter.rotate(a)
            painter.drawLine(x_start, 0, x_end, 0)

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


    def draw_title(self, painter, title):
        painter.save()

        r_height = self.config.title_font_size + 20
        r = QRect(0, self.height() - r_height, self.width(), r_height)
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, title)

        painter.restore()
