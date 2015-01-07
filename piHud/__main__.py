
import sys
from PiHud import PiHud
from PyQt4 import QtGui


def run():
	
	
	# Start QT event loop, exit upon return
	app = QtGui.QApplication(sys.argv)
	pihud = PiHud()
	sys.exit(app.exec_())



if __name__ == "__main__":
	run()
