
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
            self.__add_existing_page(configs)

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

        self.menu.addAction("New Page", self.add_page)
        self.menu.addAction("Delete Page", self.delete_page)

        # ===================== Start =====================

        self.goto_page(0) # calls connection.start()
        self.setWindowTitle("PiHud")
        self.showFullScreen()


    def __page(self):
        return self.stack.currentWidget()


    def __index(self):
        return self.stack.currentIndex()


    def __count(self):
        return self.stack.count()


    # ========= Widget Actions =========


    def __add_existing_widget(self, page, config):
        # make a widget from the given config
        widget = Widget(page, config)
        # add it to the page
        page.widgets.append(widget)


    def add_widget(self, command):
        # make a default config for this command
        config = self.global_config.make_config(command)
        # register the new config with this page of configs
        self.global_config.pages[self.__index()].append(config)
        # construct a new widget on this page
        self.__add_existing_widget(self.__page(), config)


    def delete_widget(self, page, widget):
        # called by the pages themselves
        page.widgets.remove(widget)
        p = self.stack.indexOf(page)
        self.global_config.pages[p].remove(widget.config)
        widget.deleteLater()


    # ========= Page Actions =========


    def __add_existing_page(self, configs=None):
        """ adds a page and fills with the given widgets """
        page = Page(self.stack, self)

        if configs is not None:
            for config in configs:
                self.__add_existing_widget(page, config)

        self.stack.addWidget(page)


    def add_page(self):
        """ adds a new (empty) page to the end of the page stack """
        self.__add_existing_page()
        self.global_config.pages.append([])
        self.goto_page(self.__count() - 1)



    def delete_page(self):
        if self.__count() > 1:
            page = self.__page()

            for widget in page.widgets:
                self.delete_widget(page, widget)

            self.stack.removeWidget(page)
            page.deleteLater()
            self.goto_page(self.__index())


    def goto_page(self, p):
        p = p % len(self.stack)
        if p != self.__index():
            self.connection.stop()
            self.connection.unwatch_all()

            # switch page
            self.stack.setCurrentIndex(p)
            self.pageMarker.set(self.__count(), self.__index())

            for widget in self.__page().widgets:
                pass

            self.connection.start()


    def next_page(self):
        """ cycle through the screen stack """
        self.goto_page(self.__index() + 1)


    # ========= Window Actions =========


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))
        if action is not None:
            command = action.data().toPyObject()
            # if this is a command creation action, make the new widget
            # there's got to be a better way to do this...
            if command is not None:
                self.add_widget(command)


    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Escape:
            self.close()

        elif key == QtCore.Qt.Key_Tab:
            self.next_page()


    def closeEvent(self, e):
        quit()
