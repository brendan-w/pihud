
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
        self.red_color = QColor(config["redline_color"])
        self.brush     = QBrush(self.color)
        self.pen       = QPen(self.color)
        self.red_pen   = QPen(self.red_color)

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(3)
        self.red_pen.setWidth(3)

        self.scale = scale(config["min"], config["max"], config["scale_step"])
        self.str_scale, self.multiplier = str_scale(self.scale, config["scale_mult"])

        self.red_offset = self.width()
        if config["redline"] is not None:
            self.red_offset  = map_value(config["redline"], config["min"], config["max"], 0, 270)


    def render(self, v):
        # approach the value
        self.value += (v - self.value) / 4
        self.update()


    def sizeHint(self):
        return QtCore.QSize(400, 100)


    def paintEvent(self, e):

        w = self.width()
        h = self.height()

        self.__scale_offsets = map_scale(self.scale, 0, self.width())
        self.__t_height = self.config["font_size"] + 8
        self.__bar_height = max(0, h - (2 * self.__t_height))

        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        self.draw_marks(painter)
        if self.config["numerals"]:
            self.draw_multiplier(painter)
            self.draw_numbers(painter)
        self.draw_bar(painter)

        painter.end()


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.width(), self.__t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        painter.restore()


    def draw_marks(self, painter):

        # border
        painter.save()

        r = QRect(1, self.__t_height, self.width() - 2, self.__bar_height)
        painter.drawRect(r)

        painter.restore()

        # marks
        for x in self.__scale_offsets:
            painter.save()

            painter.translate(x, self.__t_height)

            painter.drawLine(0, 0, 0, self.__bar_height)

            painter.restore()


    def draw_multiplier(self, painter):
        if self.multiplier > 1:
            painter.save()

            painter.setFont(self.note_font)
            s = "x" + str(self.multiplier)
            r = QRect(0, 0, self.width(), self.__t_height)
            painter.drawText(r, Qt.AlignRight | Qt.AlignVCenter, s)

            painter.restore()


    def draw_numbers(self, painter):
        for x, v in zip(self.__scale_offsets, self.str_scale):
            pass


    def draw_bar(self, painter):
        painter.save()

        painter.setBrush(self.brush)

        v = map_value(self.value, self.config["min"], self.config["max"], 1, self.width() - 2)
        r = QRect(1, self.__t_height, v, self.__bar_height)
        painter.drawRect(r)

        painter.restore()
