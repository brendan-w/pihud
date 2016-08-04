
import obd
from widgets import widgets
from PyQt4 import QtCore, QtGui


class Widget(QtGui.QWidget):

    def __init__(self, parent, config):
        super(Widget, self).__init__(parent)
        self.config = config

        # temporary coloring until display widgets get implemented
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 255, 50))
        # self.setPalette(palette)

        # make the context menu
        self.menu = QtGui.QMenu()
        self.menu.addAction(self.config["sensor"]).setDisabled(True)

        subMenu = self.menu.addMenu("Widget Type")
        for w in widgets:
            a = subMenu.addAction(w)
            a.setData(widgets[w])

        self.menu.addAction("Delete Widget", self.delete)

        # instantiate the requested graphics object
        self.graphics = widgets[config["type"]](self, config)

        self.move(self.position())
        self.show()


    def sizeHint(self):
        if (self.config['w'] is not None) and \
           (self.config['h'] is not None):
            size = QtCore.QSize(self.config['w'], self.config['h'])
            self.graphics.setFixedSize(size)
            return size
        else:
            s = self.graphics.sizeHint()
            self.config['w'] = s.width()
            self.config['h'] = s.height()
            return s


    def position(self):
        return QtCore.QPoint(self.config['x'], self.config['y'])


    def moveEvent(self, e):
        pos = e.pos()
        self.config['x'] = pos.x()
        self.config['y'] = pos.y()


    def delete(self):
        self.parent().delete_widget(self)


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


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))


    def get_command(self):
        s = self.config["sensor"]
        if s in obd.commands:
            return obd.commands[s]
        else:
            raise KeyError("'%s' is not a valid OBDCommand" % s)


    def render(self, response):
        if not response.is_null():
            self.graphics.render(response)
