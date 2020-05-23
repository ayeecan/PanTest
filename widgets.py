from PySide2 import QtGui, QtCore, QtWidgets
from maya import cmds

clickLeft  = QtCore.Qt.LeftButton
clickMid   = QtCore.Qt.MidButton
clickRight = QtCore.Qt.RightButton
altKey     = QtCore.Qt.AltModifier

red = QtGui.QColor(255, 0, 0)

class drawGrp(QtWidgets.QGraphicsWidget):
    def __init__(self, parent):
        super(drawGrp, self).__init__(parent)
        widthValue  = 200
        heightValue = 200
                
        bg = QtGui.QPainter()
        bg.setBackground(QtGui.QBrush(red, QtCore.Qt.SolidPattern))
        self.paint(bg, QtWidgets.QStyleOptionGraphicsItem())
        self.setAutoFillBackground(True)
        
        self.setGeometry(0, 0, widthValue, heightValue)
        
        self.centerWidth  = self.boundingRect().width()  / 2
        self.centerHeight = self.boundingRect().height() / 2
        self.setTransformOriginPoint(self.centerWidth, self.centerHeight)
        
        self.resetPos()
        
    def resetPos(self):
        '''Reset position and scale'''
        self.setScale(1.0)
        self.setPos(0 - self.centerWidth, 0 - self.centerHeight)
        
    def mousePressEvent(self, event):
        '''Override MOUSEPRESS event'''
        self.__mousePressPos = None
        self.__mouseMovePos  = None
        
        if event.button() == clickMid or clickRight:
            self.__mousePressPos = event.scenePos()
            self.__mouseMovePos  = event.scenePos()
        else:
            super(drawGrp, self).mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        '''
        Override MOUSEMOVE event
        Alt + middle click = pan
        Alt + right  click = zoom
        '''
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        
        #pan
        if event.buttons() == clickMid and modifiers == altKey:
            curPos = self.mapToScene(self.pos())
            globalPos = event.scenePos()
            diff = (globalPos - self.__mouseMovePos) * self.scale()
            newPos = self.mapFromScene(curPos + diff)
            self.setPos(newPos)
            self.__mouseMovePos = globalPos
                    
        #zoom    
        if event.buttons() == clickRight and modifiers == altKey:
            globalPos = event.scenePos()
            diff = globalPos - self.__mouseMovePos
            curValue = diff.manhattanLength()
            
            if (diff.x() + diff.y()) < 0:
                fixedValue = curValue * -1
            else:
                fixedValue = curValue
                
            zoomSpeed = 0.05
            if fixedValue > 0:
                newValue = zoomSpeed
            elif fixedValue < 0:
                newValue = -(zoomSpeed)
            else:
                newValue = fixedValue
                
            scaleFactor = self.scale() + newValue
            #stops inversion of widget
            finalFactor = 0.5 if scaleFactor < 0.5 else scaleFactor
            self.setScale(finalFactor)
            
        else:
            super(drawGrp, self).mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        '''Override MOUSERELEASE event'''
        if self.__mousePressPos is not None:
            moved = event.scenePos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
        else:
            super(drawGrp, self).mouseReleaseEvent(event)
            
class drawBtn(QtWidgets.QGraphicsRectItem):    
    def __init__(self, parent, colour):
        super(drawBtn, self).__init__(parent)
        
        penWidth = 2
        self.setBrush(QtGui.QBrush(colour, QtCore.Qt.SolidPattern))
        self.setPen(QtGui.QPen(colour, penWidth, QtCore.Qt.SolidLine))
        self.setRect(0, 0, 20, 20)
        
    def mousePressEvent(self, event):
        '''Override MOUSEPRESS event'''
        self.__mousePressPos = None
        self.__mouseMovePos  = None
        
        if event.button() == clickLeft:
            self.__mousePressPos = event.scenePos()
            self.__mouseMovePos  = event.scenePos()
            
    def mouseMoveEvent(self, event):
        '''Override MOUSEMOVE event'''
        if event.buttons() == clickLeft:
            curPos = self.mapToScene(self.pos())
            globalPos = event.scenePos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromScene(curPos + diff)
            self.setPos(newPos)
            self.__mouseMovePos = globalPos
        else:
            super(drawBtn, self).mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        '''Override MOUSERELEASE event'''
        if self.__mousePressPos is not None:
            moved = event.scenePos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
        else:
            super(drawBtn, self).mouseReleaseEvent(event)