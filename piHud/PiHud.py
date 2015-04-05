
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
        for configs in global_config["pages"]:
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

        self.menu.addAction("New Page", self.__add_page)
        self.menu.addAction("Delete Page", self.__delete_page)

        self.menu.addSeparator()

        self.menu.addAction("Save Layout", self.__save)

        # ===================== Start =====================

        self.timer = QtCore.QBasicTimer()
        self.setWindowTitle("PiHud")
        self.showFullScreen()

        self.start()


    def __page(self):
        return self.stack.currentWidget()


    def __index(self):
        return self.stack.currentIndex()


    def __count(self):
        return self.stack.count()


    def __save(self):
        pages = []

        for i in range(self.__count()):
            page = self.stack.widget(i)
            current_page = []
            for widget in page.widgets:
                current_page.append(widget.config)
            pages.append(current_page)

        self.global_config.save(pages)


    # ========= Main loop =========


    def timerEvent(self, event):
        page = self.__page()

        for widget in page.widgets:
            r = self.connection.query(widget.get_command())
            widget.render(r)


    def start(self):
        # watch the commands on this page
        for widget in self.__page().widgets:
            self.connection.watch(widget.get_command())

        self.connection.start()
        self.timer.start(1000/30, self)


    def stop(self):
        self.timer.stop();
        self.connection.stop()
        self.connection.unwatch_all()


    def restart(self):
        self.stop()
        self.start()


    # ========= Widget Actions =========


    def __add_existing_widget(self, page, config):
        # make a widget from the given config
        widget = Widget(page, config)
        # add it to the page
        page.widgets.append(widget)


    def __add_widget(self, command):
        # make a default config for this command
        config = self.global_config.make_config(command)

        # construct a new widget on this page
        self.__add_existing_widget(self.__page(), config)

        # register the new command
        self.restart()


    def delete_widget(self, page, widget):
        # called by the pages themselves
        page.widgets.remove(widget)
        p = self.stack.indexOf(page)
        widget.deleteLater()

        # reload this page again, to unwatch (if neccessary,
        # since multiple widgets could be using the same command)
        self.restart()


    # ========= Page Actions =========


    def __add_existing_page(self, configs=None):
        """ adds a page and fills with the given widgets """
        page = Page(self.stack, self)

        if configs is not None:
            for config in configs:
                self.__add_existing_widget(page, config)

        self.stack.addWidget(page)


    def __add_page(self):
        """ adds a new (empty) page to the end of the page stack """
        self.__add_existing_page()
        self.goto_page(self.__count() - 1)



    def __delete_page(self):
        if self.__count() > 1:

            self.stop()

            page = self.__page()

            for widget in page.widgets:
                self.delete_widget(page, widget)

            self.stack.removeWidget(page)
            page.deleteLater()
            self.goto_page(self.__index()) # calls start()



    def goto_page(self, p):
        p = p % len(self.stack)

        self.stop()

        # switch page
        self.stack.setCurrentIndex(p)
        self.pageMarker.set(self.__count(), self.__index())

        self.start()


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
                self.__add_widget(command)


    def keyPressEvent(self, e):
        key = e.key()

        if key == QtCore.Qt.Key_Escape:
            self.stop()
            self.close()

        elif key == QtCore.Qt.Key_Tab:
            self.next_page()


    def closeEvent(self, e):
        quit()
