
from PyQt4 import QtGui, QtCore


class Slider(QtGui.QWidget):
	def __init__(self, parent):
		super(Slider, self).__init__(parent)
		self.setAutoFillBackground(True)

		self.screenRect = QtGui.QApplication.desktop().screen().rect()
		height = 10
		color = QtGui.QColor(255, 255, 255)

		p = self.palette()
		p.setColor(self.backgroundRole(), color)
		self.setPalette(p)

		# make full width, and move to bottom of screen
		self.setFixedWidth(40)
		self.setFixedHeight(10)




class PageMarker(QtGui.QWidget):
	def __init__(self, parent):
		super(PageMarker, self).__init__(parent)
		self.setAutoFillBackground(True)

		self.screenRect = QtGui.QApplication.desktop().screen().rect()
		height = 10
		color = QtGui.QColor(255, 255, 255, 40)

		p = self.palette()
		p.setColor(self.backgroundRole(), color)
		self.setPalette(p)

		# make full width, and move to bottom of screen
		self.setFixedWidth(self.screenRect.width())
		self.setFixedHeight(height)
		self.move(0, self.screenRect.height() - height)


		self.mover = Slider(self)
