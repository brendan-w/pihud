
import obd
import widgets
from PyQt4 import QtCore, QtGui


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

        # start python-OBDs event loop going
        self.connection.start()


    def __make_widget(self, config):
        """ produces a widget object from the given config """
        # create new widget of the correct type
        widget = widgets.__dict__[config.class_name](self, config)
        
        # register the render function with python-OBD
        self.connection.watch(config.command, widget.render)

        # perform first render to ensure the widget gets displayed
        widget.render(self.connection.query(config.command))

        self.widgets.append(widget)


    def rewatch(self):
        """ called when switching screens """
        for widget in self.widgets:
            command = widget.config.command
            self.connection.watch(command, widget.render)
            widget.render(self.connection.query(command))


    def unwatch(self):
        """ called when switching screens """
        self.connection.unwatch_all()


    def make_default_widget(self, command):
        """ creates a new widget with a default config """
        widget_config = self.page_config.add_widget(command)
        self.__make_widget(widget_config)
        self.page_config.save()


    def delete_widget(self, widget):
        """ deletes a widget object and its config entry """
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
