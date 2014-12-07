
import obd
import widgets
from PyQt4 import QtCore, QtGui


class MainScreen(QtGui.QWidget):
    """ manages (and is a factory for) SVGWidgets """

    def __init__(self, parent, connection, config):
        super(MainScreen, self).__init__(parent)
        
        # enable dragging and dropping of widgets
        self.setAcceptDrops(True)

        self.widgets = []
        self.connection = connection
        self.config = config

        # create widgets based on the config file
        for widget_config in self.config.widget_configs:
            self.make_widget(widget_config)
        
        # create the context menu
        self.menu = QtGui.QMenu()
        if len(self.connection.supported_commands) > 0:
            for command in self.connection.supported_commands:
                a = self.menu.addAction("New %s" % command.name)
                a.setData(command)
        else:
            a = self.menu.addAction("No sensors available")
            a.setDisabled(True)

        # start python-OBDs event loop going
        self.connection.start()


    def make_widget(self, config):
        """ produces a widget object from the given config """
        # create new widget of the correct type
        widget = widgets.__dict__[config.class_name](self, config)
        
        # register the render function with python-OBD
        self.connection.watch(config.command, widget.render)

        # perform first render to ensure the widget gets displayed
        widget.render(self.connection.query(config.command))

        self.widgets.append(widget)


    def make_default_widget(self, command):
        """ creates a new widget with a default config """
        widget_config = self.config.add_widget(command)
        self.make_widget(widget_config)
        self.config.save()


    def delete_widget(self, widget):
        """ deletes a widget object and its config entry """
        self.widgets.remove(widget)
        self.config.delete_widget(widget.config)
        widget.deleteLater()
        self.config.save()


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))
        if action is not None:
            command = action.data().toPyObject()
            self.make_default_widget(command)


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        # get relative position of mouse from mimedata
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))

        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()

        self.config.save()
