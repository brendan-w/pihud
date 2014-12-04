
import obd
import widgets
from PyQt4 import QtCore, QtGui
from Config import Config_File


class MainScreen(QtGui.QWidget):

    def __init__(self, parent, connection):
        super(MainScreen, self).__init__(parent)
        self.setAcceptDrops(True)

        self.widgets = []
        self.connection = connection
        self.config_file = Config_File("piHud/config.json")

        for config in self.config_file.widget_configs:
            self.createWidget(config)

        # testing purposes only
        for widget in self.widgets:
            widget.render(self.connection.query(widget.command))


    def createWidget(self, config):
        # create new widget of the correct type
        widget = widgets.__dict__[config.class_name](self, config)
        
        # register the render function with python-OBD
        self.connection.watch(config.command, widget.render)
        
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

        self.config_file.save()
