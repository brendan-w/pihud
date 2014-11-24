import sys
from PyQt4 import QtGui, QtCore
from layout import Example


class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")

		# define the color palette
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
		self.setPalette(palette)

		self.setCentralWidget(Example(self))

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
