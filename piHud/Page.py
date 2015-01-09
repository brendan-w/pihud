
from PyQt4 import QtCore, QtGui


class Page(QtGui.QWidget):
    """ A container and dropevent catcher for widgets """

    def __init__(self, parent):
        super(Page, self).__init__(parent)
        self.setAcceptDrops(True)
        self.widgets = []
        self.show()


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        # get relative position of mouse from mimedata
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))

        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()


    def delete_widget(self, widget):
        self.parent().delete_widget(self, widget)
