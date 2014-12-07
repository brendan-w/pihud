
from PyQt4 import QtGui, QtCore


class PageMarker(QtGui.QWidget):
	def __init__(self, parent):
		super(PageMarker, self).__init__(parent)

		height = 10
		bg_color = QtGui.QColor(255, 255, 255, 50)
		fg_color = QtGui.QColor(255, 255, 255, 70)
		self.screenRect = QtGui.QApplication.desktop().screen().rect()

		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), bg_color)
		self.setPalette(p)

		# make full width, and move to bottom of screen
		self.setFixedWidth(self.screenRect.width())
		self.setFixedHeight(height)
		self.move(0, self.screenRect.height() - height)


		# the marker itself
		self.marker = QtGui.QWidget(self)

		self.marker.setAutoFillBackground(True)
		p = self.marker.palette()
		p.setColor(self.marker.backgroundRole(), fg_color)
		self.marker.setPalette(p)

		self.marker.setFixedHeight(height)
		self.set(1, 0)
		

	def set(self, n, p):
		inc = self.screenRect.width() / n
		self.marker.setFixedWidth(inc)
		self.marker.move(inc * p, 0)
