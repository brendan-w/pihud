
import obd
import widgets
from PyQt4 import QtCore, QtGui


class MainScreen(QtGui.QWidget):

    def __init__(self, parent, connection, config):
        super(MainScreen, self).__init__(parent)
        self.setAcceptDrops(True)

        self.widgets = []
        self.connection = connection
        self.config = config

        for widget_config in self.config.widget_configs:
            self.createWidget(widget_config)

        # start python-OBDs event loop going
        self.connection.start()


    def createWidget(self, config):
        # create new widget of the correct type
        widget = widgets.__dict__[config.class_name](self, config)
        
        # register the render function with python-OBD
        self.connection.watch(config.command, widget.render)

        # perform first render to ensure the widget gets displayed
        widget.render(self.connection.query(config.command))

        self.widgets.append(widget)


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
