import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg


class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")

		# define the color palette
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
		self.setPalette(palette)

		p = pg.PlotWidget(x=[1,2], y=[3,4], name="asdf");
		self.setCentralWidget(p)

		#grid = QtGui.QGridLayout()
		#self.setLayout(grid)

		self.showFullScreen()

	def keyPressEvent(self, event):
		key = event.key()

		if key == QtCore.Qt.Key_Escape:
			quit()


def main():
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()

	# Start QT event loop, exit upon return
	sys.exit(app.exec_())
	

if __name__ == "__main__":
	main()
