
import sys
import obd
from Gui import Gui
from MainScreen import MainScreen
from Config import Config
from PyQt4 import QtGui, QtCore


# pygal optimizations
try:
	from pygal.svg import Svg
	Svg.add_scripts = lambda *args: None # completely disable the JS generator
except:
	pass


class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")

		# define the color palette
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
		self.setPalette(palette)
		
		# read the config file
		self.config = Config("piHud/config.json")

		# init OBD conncetion
		obd.debug.console = True
		self.connection = obd.Async(self.config.port)

		# create the context menu
		self.menu = QtGui.QMenu()

		if len(self.connection.supported_commands) > 0:
			for command in self.connection.supported_commands:
				a = self.menu.addAction("New %s" % command.name)
				a.setData(command)
		else:
			a = self.menu.addAction("No sensors available")
			a.setDisabled(True)

		# make a screen stack
		self.screenStack = QtGui.QStackedWidget(self)
		self.setCentralWidget(self.screenStack)

		# the various screens
		mainScreen = MainScreen(self, self.connection, self.config)
		guiScreen = Gui(self, self.connection, self.config)
		
		# add them to the stack
		self.screenStack.addWidget(mainScreen)
		self.screenStack.addWidget(guiScreen)


		self.screenStack.setCurrentWidget(mainScreen)
		self.showFullScreen()


	def contextMenuEvent(self, e):
		action = self.menu.exec_(self.mapToGlobal(e.pos()))
		if action is not None:
			print "ACTION", action.data().toPyObject()


	def keyPressEvent(self, event):
		key = event.key()

		if key == QtCore.Qt.Key_Escape:
			self.close()

		elif key == QtCore.Qt.Key_Tab:
			# cycle through the screen stack
			next_index = (self.screenStack.currentIndex() + 1) % len(self.screenStack)
			self.screenStack.setCurrentIndex(next_index)


	def closeEvent(self, e):
		self.connection.close()
		quit()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()

	# Start QT event loop, exit upon return
	sys.exit(app.exec_())
