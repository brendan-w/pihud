
from PyQt4 import QtCore, QtGui, QtSvg


class SVGWidget(QtSvg.QSvgWidget):

    def __init__(self, parent, config):
        super(SVGWidget,self).__init__(parent)
        self.config = config
        self.command = config.command

        # set size and position
        if config.position is not None:
            self.move(config.position["x"], config.position["y"])
        else:
            self.default_position()
            config.position = { "x":self.x(), "y":self.y() }

        if config.dimensions is not None:
            self.setFixedWidth(config.dimensions['x'])
            self.setFixedHeight(config.dimensions['y'])
        else:
            self.default_dimensions()
            config.dimensions = { "x":self.width(), "y":self.height() }


        # make the context menu
        self.menu = QtGui.QMenu()

        a = self.menu.addAction(self.config.command.name)
        a.setDisabled(True)
        self.menu.addAction("Delete Widget", self.delete)

        self.show()


    def default_position(self):
        self.move(0, 0)


    def default_dimensions(self):
        self.setFixedWidth(200)
        self.setFixedHeight(200)


    def moveEvent(self, e):
        """ keep the position in the config up to date """
        self.config.position = { 'x':e.pos().x(), 'y':e.pos().y() }


    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:

            mimeData = QtCore.QMimeData()
            mimeData.setText('%d,%d' % (e.x(), e.y()))

            # show the ghost image while dragging
            pixmap = QtGui.QPixmap.grabWidget(self)
            painter = QtGui.QPainter(pixmap)
            painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
            painter.end()

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.pos())

            drag.exec_(QtCore.Qt.MoveAction)


    def mousePressEvent(self, e):
        super(SVGWidget, self).mousePressEvent(e)


    def showChart(self, chart):
        """ handles loading of pygal SVGs """

        # PyQt has a rendering issue with the following CSS
        # https://github.com/brendanwhitfield/piHud/issues/2
        chart.style.stroke_dasharray = ""

        # they have a 'no_prefix' setting, but PyQt couldn't render the result,
        # so the ID is set to be as short as possible (to save memory)
        chart.uuid = ""

        # we don't need this
        chart.show_legend = False

        # set the title
        chart.title = self.config.title

        # disable the no data text
        chart.no_data_text = ""

        # set font sizes
        chart.major_label_font_size = self.config.label_font_size
        chart.label_font_size       = self.config.label_font_size
        chart.title_font_size       = self.config.title_font_size

        # set the range
        chart.range = [self.config.min, self.config.max]

        # format decimal values appropriatley
        chart.human_readable = True

        # match the SVG dimensions to the Widget dimensions
        chart.width = self.width()
        chart.height = self.height()

        # render the SVG string
        svg = chart.render()

        # wrap in PyQt byteArray
        byteArray = QtCore.QByteArray(svg)
        self.load(byteArray)


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))


    def delete(self):
        self.parent().delete_widget(self)

    def render(self, response):
        """ this function should be overriden in subclass """
        pass
