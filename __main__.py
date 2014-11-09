import sys
from PyQt4 import QtGui


class PiHud(QtGui.QMainWindow):
	def __init__(self):
		super(PiHud, self).__init__()

		self.setWindowTitle("PiHud")
		self.showFullScreen()


def main():
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()

	# Start
	sys.exit(app.exec_())
	

if __name__ == "__main__":
	main()