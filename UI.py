from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtGui, QtCore
from maya import cmds

import widgets as wdg
reload(wdg)

white = QtGui.QColor(255, 255, 255)
black = QtGui.QColor(  0,   0,   0)
red   = QtGui.QColor(255,   0,   0)

class panTestWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(panTestWindow, self).__init__(parent = parent)
        
        self._editMode = False
        
        wdgMain = QtWidgets.QWidget(self)
        self.setCentralWidget(wdgMain)
        self.setWindowTitle("PanTest")
        self.resize(700, 500)
        
        #background
        self.bg = QtWidgets.QGraphicsScene()
        self.bg.setSceneRect(-5, -5, 10, 10)
        self.bg.setBackgroundBrush(QtGui.QBrush(white, QtCore.Qt.SolidPattern))
        viewBg = QtWidgets.QGraphicsView(self.bg)
        
        self.drawCrosshair()
        
        backboard = wdg.drawGrp(None)
        self.bg.addItem(backboard)
        
        moveBtn = wdg.drawBtn(None, red)
        moveBtn.setParentItem(backboard)
        
        resetBtn = QtWidgets.QPushButton('Reset', self)
        resetBtn.released.connect(backboard.resetPos)
        
        finalLay = QtWidgets.QVBoxLayout(wdgMain)
        finalLay.addWidget(viewBg)
        finalLay.addWidget(resetBtn)
        
    def drawCrosshair(self):
        axisX = self.drawLine(black, True)
        self.bg.addItem(axisX)
        
        axisY = self.drawLine(black, False)
        self.bg.addItem(axisY)
    
    def drawLine(self, colour, horizontal = True):
        length = 10
        penWidth = 1
        if horizontal:
            lineX1, lineY1, lineX2, lineY2 = -(length), 0, length, 0
        else:
            lineX1, lineY1, lineX2, lineY2 = 0, -(length), 0, length

        line = QtWidgets.QGraphicsLineItem()
        line.setPen(QtGui.QPen(colour, penWidth, QtCore.Qt.SolidLine))
        line.setLine(lineX1, lineY1, lineX2, lineY2)
        
        return line
                
def launchUI():
    window = None
    uiName = 'panTest'
    
    if uiName in globals() and globals()[uiName].isVisible():
        window = globals()[uiName]
        if window.isVisible():
            window.show()
            window.raise_()
            return None
            
    nuWindow = panTestWindow()
    globals()[uiName] = nuWindow
    nuWindow.show(dockable = True, floating = True)