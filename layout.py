from PyQt4 import QtCore, QtGui,QtSvg
import pygal

class Button(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):
      
        super(Button, self).mousePressEvent(e)
        
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'

class SVGWidget(QtSvg.QSvgWidget):
    
    def __init__(self,parent, file):
        super(SVGWidget,self).__init__(parent)
        super(SVGWidget,self).load(file)

    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):
      
        super(SVGWidget, self).mousePressEvent(e)


class Example(QtGui.QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        self.draggables = []

        self.initUI()
        
    def initUI(self):

        self.setAcceptDrops(True)

        button = Button('Button', self)
        button.move(600, 65)
        self.draggables.append(button);

        bar_chart = pygal.Bar(width= 300 ,height = 200)                                
        bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]) 
        chart = QtCore.QByteArray (bar_chart.render())
        # bar_chart.render_to_file('bar_chart.svg') 

        svg1 =  SVGWidget(self,chart)
        self.draggables.append(svg1);

        self.setWindowTitle('PyHud')
        self.setGeometry(300, 300, 280, 150)
        self.show()

    def dragEnterEvent(self, e):
      
        e.accept()

    def dropEvent(self, e):

        position = e.pos()        
        e.source().move(position)  

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())
