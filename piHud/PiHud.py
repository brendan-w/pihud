
import os
import obd
from Page import Page
from Config import Config
from PageMarker import PageMarker
from PyQt4 import QtGui, QtCore


# RPi GPIO 
try:
	import RPi.GPIO as GPIO
except:
	pass




class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")

		# define the color palette
		palette = self.palette()
		palette.setColor(self.backgroundRole(), QtCore.Qt.black)
		self.setPalette(palette)
		
		# read the config file
		config_path = os.path.join(os.path.expanduser("~"), "pihud.rc")
		self.config = Config(config_path)


		try:
			pin = self.config.page_adv_pin
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GIO.add_event_detect(pin, GPIO.FALLING, callback=self.__next_page, bouncetime=200)
		except:
			pass


		# init OBD conncetion
		obd.debug.console = True
		self.connection = obd.Async(self.config.port)
		for i in range(26):
			self.connection.supported_commands.append(obd.commands[1][i])

		# make a screen stack
		self.stack = QtGui.QStackedWidget(self)
		self.setCentralWidget(self.stack)
		self.pageMarker = PageMarker(self)

		# read the config and make pages
		if len(self.config.pages) > 0:
			for page in self.config.pages:
				self.__add_page(page)
		else:
			self.__add_empty_page()

		# create the context menu for adding widgets and pages
		self.init_context_menu()

		# save any default data that was missing when the config was imported
		self.config.save()

		# start python-OBDs event loop going
		self.connection.start()
		self.__goto_page(0)

		if not self.config.demo: # this is ugly, but I have a deadline
			self.timer = QtCore.QBasicTimer()
			self.timer.start(1000/20, self)

		self.showFullScreen()


	def timerEvent(self, event):
		self.stack.currentWidget().render()


	def __add_page(self, page_config):
		page = Page(self, self.connection, page_config)
		self.stack.addWidget(page)


	def __add_empty_page(self):
		page_config = self.config.add_page()
		self.__add_page(page_config)
		self.__goto_page(self.stack.count() - 1)
		self.config.save()


	def __delete_page(self):
		if self.stack.count() > 1:
			page = self.stack.currentWidget()
			page.delete_all_widgets()
			self.stack.removeWidget(page)
			self.config.delete_page(page.page_config)
			page.deleteLater()
			self.config.save()

			self.__goto_page(self.stack.currentIndex())


	def __goto_page(self, p):
		if p != self.stack.currentIndex:
			self.stack.setCurrentIndex(p)
			self.pageMarker.set(self.stack.count(), self.stack.currentIndex())


	def __next_page(self):
		# cycle through the screen stack
		next_index = (self.stack.currentIndex() + 1) % len(self.stack)
		self.__goto_page(next_index)


	def init_context_menu(self):
		# create the context menu
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



	def contextMenuEvent(self, e):
		action = self.menu.exec_(self.mapToGlobal(e.pos()))
		if action is not None:
			command = action.data().toPyObject()
			# if this is a command creation action, make the new widget
			# there's got to be a better way to do this...
			if command is not None:
				self.stack.currentWidget().make_default_widget(command)


	def keyPressEvent(self, event):
		key = event.key()

		if key == QtCore.Qt.Key_Escape:
			self.close()

		elif key == QtCore.Qt.Key_Tab:
			self.__next_page()


	def closeEvent(self, e):
		self.connection.close()
		quit()
