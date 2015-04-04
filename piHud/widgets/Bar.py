
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from util import scale, map_scale, map_value, scale_offsets, str_scale


class Bar_Horizontal(QWidget):
    def __init__(self, parent, config):
        super(Bar_Horizontal, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font      = QFont()
        self.note_font = QFont()
        self.color     = QColor(config["color"])
        self.brush     = QBrush(self.color)
        self.pen       = QPen(self.color)

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(3)

        s = scale(config["min"], config["max"])

        self.abs_angles = map_scale(s, 0, 270)
        self.offset_angles = scale_offsets(self.abs_angles)
        self.str_scale, self.multiplier = str_scale(s)


    def render(self, v):
        # approach the value
        self.value += (v - self.value) / 4
        self.update()


    def sizeHint(self):
        return QtCore.QSize(400, 100)


    def paintEvent(self, e):

        w = self.width()
        h = self.height()

        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)

        painter.end()


    def draw_title(self, painter):
        painter.save()

        r_height = self.config["font_size"] + 20
        r = QRect(0, 0, self.width(), r_height)
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, self.config["title"])

        painter.restore()