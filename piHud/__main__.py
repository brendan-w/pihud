
import sys
import obd
from MainScreen import MainScreen
from Config import Config
from PyQt4 import QtGui, QtCore


# pygal optimizations
try:
	from pygal.svg import Svg
	# pygal always dumps its configs to JS and embeds them in the SVGs
	# we don't need that...
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

		# make a screen stack
		self.screenStack = QtGui.QStackedWidget(self)
		self.setCentralWidget(self.screenStack)

		# the various screens
		mainScreen = MainScreen(self, self.connection, self.config)
		
		# add them to the stack
		self.screenStack.addWidget(mainScreen)


		self.screenStack.setCurrentWidget(mainScreen)
		self.showFullScreen()


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
