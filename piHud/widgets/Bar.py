
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from util import map_value, in_range


class Bar_Horizontal(QWidget):
    def __init__(self, parent, config):
        super(Bar_Horizontal, self).__init__(parent)

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


    def render(self, v):
        # approach the value
        self.value += (v - self.value) / 4
        self.update()


    def sizeHint(self):
        return QSize(400, 60)


    def paintEvent(self, e):

        w = self.width()
        h = self.height()

        # recompute new values
        self.__l = 2            # left X value
        self.__r = w - self.__l # right X value
        self.__t_height = self.config["font_size"] + 8
        self.__bar_height = max(0, h - self.__t_height) - self.__l
        self.__value_offset = map_value(self.value,
                                        self.config["min"],
                                        self.config["max"],
                                        self.__l,
                                        self.__r)
        self.__red_offset = w
        if self.config["redline"] is not None:
            self.__red_offset = map_value(self.config["redline"],
                                          self.config["min"],
                                          self.config["max"],
                                          self.__l,
                                          self.__r)

        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        self.draw_border(painter)
        self.draw_bar(painter)

        painter.end()


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.width(), self.__t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        painter.restore()


    def draw_border(self, painter):
        painter.save()
        painter.translate(0, self.__t_height)

        if in_range(self.__red_offset, self.__l, self.__r):
            # non-red zone
            path = QPainterPath()
            path.moveTo(self.__red_offset, 0)
            path.lineTo(self.__l, 0)
            path.lineTo(self.__l, self.__bar_height)
            path.lineTo(self.__red_offset, self.__bar_height)

            painter.drawPath(path)

            # red zone
            path = QPainterPath()
            path.moveTo(self.__red_offset, 0)
            path.lineTo(self.__r, 0)
            path.lineTo(self.__r, self.__bar_height)
            path.lineTo(self.__red_offset, self.__bar_height)

            painter.setPen(self.red_pen)
            painter.drawPath(path)

        else:
            painter.drawRect(QRect(
                self.__l,
                self.__l,
                self.__r - self.__l,
                self.__bar_height,
            ))

        painter.restore()


    def draw_bar(self, painter):
        painter.save()
        painter.translate(0, self.__t_height)
        painter.setPen(self.no_pen)
        painter.setBrush(self.brush)

        if in_range(self.__red_offset, self.__l, self.__r):
            if self.__value_offset <= self.__red_offset:
                painter.drawRect(QRect(
                    self.__l,
                    0,
                    self.__value_offset,
                    self.__bar_height
                ))
            else:
                painter.drawRect(QRect(
                    self.__l,
                    0,
                    self.__red_offset,
                    self.__bar_height
                ))

                painter.setBrush(self.red_brush)
                painter.setPen(self.red_pen)

                painter.drawRect(QRect(
                    self.__red_offset,
                    0,
                    self.__value_offset - self.__red_offset,
                    self.__bar_height
                ))
        else:
            painter.drawRect(QRect(
                    self.__l,
                    0,
                    self.__value_offset,
                    self.__bar_height
            ))

        painter.restore()
