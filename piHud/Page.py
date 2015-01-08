
import obd
from widgets import widgets
from PyQt4 import QtCore, QtGui

import math # used got demo mode
from obd.utils import Response # used got demo mode
from util import map_value


class Page(QtGui.QWidget):
    """ A container and dropevent catcher for widgets """

    def __init__(self, parent):
        super(Page, self).__init__(parent)
        self.setAcceptDrops(True)
        self.widgets = []


    def __make_widget(self, config):
        """ produces a widget object from the given config """
        # create new widget of the correct type
        widget = widgets[config.class_name](self, config)
        self.connection.watch(config.command)
        self.widgets.append(widget)


    def delete_widget(self, widget):
        """ deletes a widget object and its config entry """
        
        # unwatch the command by submitting the command and the callback to be removed
        # self.connection.unwatch(widget.config.command)

        self.widgets.remove(widget)
        self.page_config.delete_widget(widget.config)
        widget.deleteLater()
        self.page_config.save()


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
