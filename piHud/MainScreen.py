
import obd
import widgets
from PyQt4 import QtCore, QtGui

import math # used got demo mode
from obd.utils import Response # used got demo mode
from util import map_value


class MainScreen(QtGui.QWidget):
    """ manages (and is a factory for) SVGWidgets """

    def __init__(self, parent, connection, page_config):
        super(MainScreen, self).__init__(parent)
        
        # enable dragging and dropping of widgets
        self.setAcceptDrops(True)

        self.widgets = []
        self.connection = connection
        self.page_config = page_config

        # create widgets based on the config file
        for widget_config in self.page_config.widget_configs:
            self.__make_widget(widget_config)

        # if in demo mode, start a timer to push values to each widget
        if page_config.config.demo:
            self.theta = 0
            self.timer = QtCore.QBasicTimer()
            self.timer.start(1000/30, self)


    def timerEvent(self, event):
        """ event loop for demo mode """
        for widget in self.widgets:
            self.theta += 0.01

            min_ = widget.config.min
            max_ = widget.config.max

            # value mapping
            value = map_value(math.cos(self.theta), -1, 1, min_, max_)

            r = Response()
            r.raw_data = "00 00 00 00"
            r.value = int(value)
            r.unit = "unit"

            widget.render(r)


    def render(self):
        for widget in self.widgets:
            r = self.connection.query(widget.config.command)
            widget.render(r)


    def __make_widget(self, config):
        """ produces a widget object from the given config """
        # create new widget of the correct type
        widget = widgets.__dict__[config.class_name](self, config)
        self.connection.watch(config.command)
        self.widgets.append(widget)


    def rewatch(self):
        """ called when switching screens """
        for widget in self.widgets:
            command = widget.config.command
            self.connection.watch(command, widget.render)
            widget.render(self.connection.query(command)) # perform initial render


    def make_default_widget(self, command):
        """ creates a new widget with a default config """
        widget_config = self.page_config.add_widget(command)
        self.__make_widget(widget_config)
        self.page_config.save()


    def delete_widget(self, widget):
        """ deletes a widget object and its config entry """
        
        # unwatch the command by submitting the command and the callback to be removed
        # self.connection.unwatch(widget.config.command)

        self.widgets.remove(widget)
        self.page_config.delete_widget(widget.config)
        widget.deleteLater()
        self.page_config.save()


    def delete_all_widgets(self):
        for widget in self.widgets:
            self.delete_widget(widget)


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        # get relative position of mouse from mimedata
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))

        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()

        self.page_config.save()
