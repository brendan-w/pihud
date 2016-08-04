
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pihud.util import map_value, in_range


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


    def render(self, response):
        # approach the value
        self.value += (response.value.magnitude - self.value) / 4
        self.update()


    def sizeHint(self):
        return QSize(400, 60)


    def paintEvent(self, e):


        painter = QPainter()
        painter.begin(self)

        self.pre_compute(painter)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        self.draw_border(painter)
        self.draw_bar(painter)

        painter.end()


    def pre_compute(self, painter):
        w = self.width()
        h = self.height()

        # recompute new values
        self.l = 2            # left X value
        self.r = w - self.l # right X value
        self.t_height = self.config["font_size"] + 8
        self.bar_height = max(0, h - self.t_height) - self.l
        self.value_offset = map_value(self.value,
                                        self.config["min"],
                                        self.config["max"],
                                        self.l,
                                        self.r)
        self.red_offset = w
        if self.config["redline"] is not None:
            self.red_offset = map_value(self.config["redline"],
                                          self.config["min"],
                                          self.config["max"],
                                          self.l,
                                          self.r)


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        painter.restore()


    def draw_border(self, painter):
        painter.save()
        painter.translate(0, self.t_height)

        if in_range(self.red_offset, self.l, self.r):
            # non-red zone
            path = QPainterPath()
            path.moveTo(self.red_offset, 0)
            path.lineTo(self.l, 0)
            path.lineTo(self.l, self.bar_height)
            path.lineTo(self.red_offset, self.bar_height)

            painter.drawPath(path)

            # red zone
            path = QPainterPath()
            path.moveTo(self.red_offset, 0)
            path.lineTo(self.r, 0)
            path.lineTo(self.r, self.bar_height)
            path.lineTo(self.red_offset, self.bar_height)

            painter.setPen(self.red_pen)
            painter.drawPath(path)

        else:
            painter.drawRect(QRect(
                self.l,
                self.l,
                self.r - self.l,
                self.bar_height,
            ))

        painter.restore()


    def draw_bar(self, painter):
        painter.save()
        painter.translate(0, self.t_height)
        painter.setPen(self.no_pen)
        painter.setBrush(self.brush)

        if in_range(self.red_offset, self.l, self.r):
            if self.value_offset <= self.red_offset:
                painter.drawRect(QRect(
                    self.l,
                    0,
                    self.value_offset,
                    self.bar_height
                ))
            else:
                painter.drawRect(QRect(
                    self.l,
                    0,
                    self.red_offset,
                    self.bar_height
                ))

                painter.setBrush(self.red_brush)
                painter.setPen(self.red_pen)

                painter.drawRect(QRect(
                    self.red_offset,
                    0,
                    self.value_offset - self.red_offset,
                    self.bar_height
                ))
        else:
            painter.drawRect(QRect(
                    self.l,
                    0,
                    self.value_offset,
                    self.bar_height
            ))

        painter.restore()




class Bar_Vertical(Bar_Horizontal):
    def __init__(self, parent, config):
        super(Bar_Vertical, self).__init__(parent, config)


    def pre_compute(self, painter):

        painter.rotate(-90)
        painter.translate(-self.height(), 0)

        # swap the X vs Y
        h = self.width()
        w = self.height()

        # recompute new values
        self.l = 2          # left X value
        self.r = w - self.l # right X value
        self.t_height = self.config["font_size"] + 8
        self.bar_height = max(0, h - self.t_height) - self.l
        self.value_offset = map_value(self.value,
                                      self.config["min"],
                                      self.config["max"],
                                      self.l,
                                      self.r)
        self.red_offset = w
        if self.config["redline"] is not None:
            self.red_offset = map_value(self.config["redline"],
                                        self.config["min"],
                                        self.config["max"],
                                        self.l,
                                        self.r)


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.height(), self.t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        painter.restore()

