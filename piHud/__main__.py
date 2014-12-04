
import sys
import obd
from MainScreen import MainScreen
from PyQt4 import QtGui, QtCore


class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")

		# define the color palette
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
		self.setPalette(palette)

		# pygal optimizations
		try:
			from pygal.svg import Svg
			Svg.add_scripts = lambda *args: None # completely disable the JS generator
		except:
			pass

		# init OBD conncetion
		# obd.debug.console = True
		self.connection = obd.Async()

		self.setCentralWidget(MainScreen(self, self.connection))
		self.showFullScreen()

	def keyPressEvent(self, event):
		key = event.key()

		if key == QtCore.Qt.Key_Escape:
			quit()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()

	# Start QT event loop, exit upon return
	sys.exit(app.exec_())
