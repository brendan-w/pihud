
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pihud.util import map_value, in_range


class Text(QWidget):
    def __init__(self, parent, config):
        super(Text, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font      = QFont()
        self.note_font = QFont()
        self.color     = QColor(config["color"])
        self.red_color = QColor(config["redline_color"])
        self.no_color  = QColor()
        self.no_color.setAlpha(0)

        self.brush     = QBrush(self.color)
        self.red_brush = QBrush(self.red_color)

        self.pen       = QPen(self.color)
        self.red_pen   = QPen(self.red_color)
        self.no_pen    = QPen(self.no_color)

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(3)
        self.red_pen.setWidth(3)

        self.red_value = config["redline"]
        if self.red_value is None:
            self.red_value = config["max"]


    def sizeHint(self):
        return QSize(300, 75)


    def render(self, v):
        self.value = v
        self.update()


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        self.t_height = self.config["font_size"] + 8

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        h = 0

        if len(self.config["title"]) > 0:
            h += self.t_height
            r = QRect(0, 0, self.width(), self.t_height)
            painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        r = QRect(0, h, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignVCenter, str(int(round(self.value))))

        painter.end()
