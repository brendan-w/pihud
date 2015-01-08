
from Page import Page
from Widget import Widget
from PageMarker import PageMarker
from PyQt4 import QtGui, QtCore



class PiHud(QtGui.QMainWindow):
    def __init__(self, global_config, connection):
        super(PiHud, self).__init__()
        self.global_config = global_config
        self.connection = connection

        # ================= Color Palette =================

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)

        # ================== Init Pages ===================

        self.pageMarker = PageMarker(self)
        self.stack      = QtGui.QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # read the config and make pages
        for configs in self.global_config.pages:
            self.__add_page(configs)

        # ================= Context Menu ==================

        self.menu = QtGui.QMenu()
        subMenu = self.menu.addMenu("Add Widget")

        if len(self.connection.supported_commands) > 0:
            for command in self.connection.supported_commands:
                a = subMenu.addAction(command.name)
                a.setData(command)
        else:
            a = subMenu.addAction("No sensors available")
            a.setDisabled(True)
        
        self.menu.addSeparator()

        self.menu.addAction("New Page", self.__add_empty_page)
        self.menu.addAction("Delete Page", self.__delete_page)

        # ===================== Start =====================

        self.__goto_page(0)
        self.connection.start()
        self.setWindowTitle("PiHud")
        self.showFullScreen()


    def __add_widget(self, page, config):
        widget = Widget(page, config)
        page.widgets.append(widget)



    def __add_default_widget(self, command):
        config = self.global_config.make_config(command)
        page = self.stack.currentWidget()
        self.global_config.pages[self.stack.currentIndex()].append(config)
        self.__add_widget(page, config)


    def __add_page(self, configs):
        """ adds a page and fills with the given widgets """

        page = Page(self)

        for config in configs:
            self.__add_widget(page, config)

        self.stack.addWidget(page)


    def __add_empty_page(self):
        """ adds a new (empty) page to the end of the page stack """
        self.__add_page([])
        self.global_config.pages.append([])
        self.__goto_page(self.stack.count() - 1)



    def __delete_page(self):
        if self.stack.count() > 1:
            page = self.stack.currentWidget()
            self.stack.removeWidget(page)

            for widget in page:
                pass

            page.deleteLater()
            # self.config.save()

            self.__goto_page(self.stack.currentIndex())


    def __goto_page(self, p):
        p = p % len(self.stack)
        if p != self.stack.currentIndex:
            self.stack.setCurrentIndex(p)
            self.pageMarker.set(self.stack.count(), self.stack.currentIndex())


    def next_page(self):
        """ cycle through the screen stack """
        self.__goto_page(self.stack.currentIndex() + 1)


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))
        if action is not None:
            command = action.data().toPyObject()
            # if this is a command creation action, make the new widget
            # there's got to be a better way to do this...
            if command is not None:
                self.__add_default_widget(command)


    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            self.close()

        elif key == QtCore.Qt.Key_Tab:
            self.next_page()


    def closeEvent(self, e):
        quit()
