import maya.OpenMayaUI
import os
import json
from functools import partial


from maya import cmds

if int( cmds.about( v=1 ) ) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction,\
    QFont, QGridLayout
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider,\
    QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction, QGridLayout
    
    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform,\
    QPaintEvent, QFont



def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



class Window_global:
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "SGMTool_imageLoader"
    title = "SGMTool Image Loader"
    width = 300
    height = 300
    
    infoPath = cmds.about(pd=True) + "/sg/sg_toolInfo/imageLoader.txt"
    makeFile( infoPath )
    
    mainGui = QMainWindow()
    
    @staticmethod
    def saveInfo( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath
        
        posX = Window_global.mainGui.pos().x()
        posY = Window_global.mainGui.pos().y()
        width  = Window_global.mainGui.width()
        height = Window_global.mainGui.height()
        
        f = open( filePath, "w" )
        json.dump( [posX, posY, width, height, Window_global.mainGui.tabWidget.getChildrenInfo(), Window_global.mainGui.tabWidget.currentIndex() ], f, True, False, False )
        f.close()
    
    
    @staticmethod
    def loadInfo( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath
        
        f = open( filePath, 'r')
        try:data = json.load( f )
        except: f.close(); return None
        f.close()
    
        if not data: return None
        
        try:
            posX = data[0]
            posY = data[1]
            width = data[2]
            height = data[3]
            
            Window_global.mainGui.resize( width, height )
            
            desktop = QApplication.desktop()
            desktopWidth = desktop.width()
            desktopHeight = desktop.height()
            if posX + width > desktopWidth: posX = desktopWidth - width
            if posY + height > desktopWidth: posY = desktopHeight - height
            if posX < 0 : posX = 0
            if posY < 0 : posY = 0
            
            Window_global.mainGui.move( posX, posY )
            
            children = data[4]
            
            for child in children:
                tabText = child["tabText"]
                imagePath = child['imagePath']
                x, y, scale, rotValue, scaleMultX = child['imagePosition']
                
                Window_global.mainGui.tabWidget.addTab(tabText)
                widgets = Window_global.mainGui.tabWidget.widget(children.index(child)).children()
                for widget in widgets:
                    if widget.__class__ == FilePathLine:
                        widget.setText( imagePath )
                    elif widget.__class__ == ImageBase:
                        widget.loadImage( imagePath )
                        widget.transInfo.x = x
                        widget.transInfo.y = y
                        widget.transInfo.scale = scale
                        widget.transInfo.rotValue = rotValue
                        widget.transInfo.scaleMultX = scaleMultX
                        widget.resize()
            
            cuIndex = data[5]
            Window_global.mainGui.tabWidget.setCurrentIndex( cuIndex )
        except:
            pass



class ImageBaseTranslateInfo():
    
    def __init__(self ):
        
        self.scale = 1
        self.fliped = False
        self.x = 0
        self.y = 0
        
        self.bScale = 1
        self.bx = 0
        self.by = 0
        
        self.pressX = 0
        self.pressY = 0
        
        self.dragMode = 0
        
        self.rotValue = 0
        self.bRotValue = 0
        
        self.shiftPressed = False
        
        self.scaleMultX = 1
        
        
    def scaleX(self):
        return self.scale * self.scaleMultX
    
    def scaleY(self):
        return self.scale
        
    
    def buttonPress(self, button, x, y ):
        
        self.bRotValue = self.rotValue
        self.bScale = self.scale
        self.pressX = x
        self.pressY = y
        self.bx = self.x
        self.by = self.y
        self.dragMode = button
    
    
    def buttonRelease(self):
        self.dragMode = 0
    
    
    def drag(self, x, y ):
        if self.dragMode == 0: return None
        
        if self.dragMode == 1:
            import math
            addRotValue = (x - self.pressX )/3.0
            self.rotValue = self.bRotValue + addRotValue
            
            if self.shiftPressed:
                elseValue = self.rotValue % 90
                if math.fabs( elseValue ) < 5:
                    self.rotValue -= elseValue
                    addRotValue -= elseValue
                elif math.fabs( elseValue ) > 85:
                    self.rotValue = self.rotValue + 90 - elseValue
                    addRotValue = addRotValue + 90 - elseValue
            
            radValue = math.radians( addRotValue )
            
            sinValue = math.sin( radValue )
            cosValue = math.cos( radValue )
            
            movedX = self.bx * cosValue - self.by * sinValue
            movedY = self.bx * sinValue + self.by * cosValue
            
            self.x = movedX
            self.y = movedY
            
            
        elif self.dragMode == 4:
            moveX = x - self.pressX
            moveY = y - self.pressY
            self.x = moveX + self.bx
            self.y = moveY + self.by
        
        elif self.dragMode == 2:
            moveX = x - self.pressX
            rect = QApplication.desktop().screenGeometry();
            height = rect.height()/4
            self.scale = self.bScale * (2**(float(moveX)/height))
            scaledValue = self.scale/  self.bScale
            
            self.x = (self.bx - self.pressX) * scaledValue + self.pressX
            self.y = (self.by - self.pressY) * scaledValue + self.pressY



class ImageBase(QLabel):

    def __init__(self, *args, **kwargs):
        
        self.transInfo = ImageBaseTranslateInfo()
        
        super(ImageBase, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        
        self.image            = QImage()
        self.imageTransformed = QImage()
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.imagePath = ""
        self.aspect = 1
        
    
    def loadImage(self, filePath ):
        
        if self.imagePath == filePath: return None
        self.imagePath = filePath
        
        self.aspect = 1
        if self.image.load(filePath): pass
        self.resize()
        

    def resize(self):
        
        trValue = QTransform().scale( self.transInfo.scaleX(), self.transInfo.scaleY() )
        trValue *= QTransform().rotate( self.transInfo.rotValue )
        imageTransformed = self.image.transformed(trValue)
        
        imageWidth = imageTransformed.width()
        imageHeight = imageTransformed.height()
        
        self.pixmap = QPixmap.fromImage( imageTransformed )
        self.label.setPixmap( self.pixmap )
        
        marginLeft = (self.width() - imageWidth)/2.0
        marginTop  = (self.height() - imageHeight)/2.0
        
        self.label.setGeometry( marginLeft + self.transInfo.x,marginTop + self.transInfo.y, imageWidth, imageHeight )
        
        
    def flip(self, pressX ):
        
        offsetX = pressX - self.width()/2
        
        self.transInfo.rotValue *= -1
        self.transInfo.x = (self.transInfo.x - offsetX)*-1 + offsetX
        self.transInfo.scaleMultX *= -1
        
        self.resize()
        
    
    def show( self ):
        self.label.show()
    

    def eventFilter( self, Obj, event ):
        
        if event.type() == QtCore.QEvent.Resize:
            self.resize()
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            pressX = event.x()-self.width()/2
            pressY = event.y()-self.height()/2
            self.transInfo.buttonPress(event.button(), pressX, pressY )
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.transInfo.x == self.transInfo.bx and self.transInfo.y == self.transInfo.by:
                pass
            self.transInfo.buttonRelease()
            Window_global.saveInfo()
        elif event.type() == QtCore.QEvent.MouseMove:
            pressX = event.x()-self.width()/2
            pressY = event.y()-self.height()/2
            self.transInfo.drag( pressX, pressY )
            self.resize()
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.flip( event.x() )
        elif event.type() == QtCore.QEvent.Wheel:
            pressX = event.x()-self.width()/2
            pressY = event.y()-self.height()/2
            self.transInfo.buttonPress( QtCore.Qt.RightButton , pressX, pressY)
            self.transInfo.drag( pressX + event.delta()/2, pressY )
            self.transInfo.buttonRelease()
            self.resize()
            Window_global.saveInfo()
            
        return True




class FilePathLine( QLineEdit ):
    def __init__(self, *args, **kwargs ):
        super( FilePathLine, self ).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.imageBase = ''
    
    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.KeyPress:
            if os.path.exists( self.text() ):
                self.imageBase.loadImage( self.text() )
                Window_global.saveInfo()
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            paths = cmds.fileDialog2( fm=1 )
            if paths:
                self.setText( paths[0] )
                self.imageBase.loadImage( self.text() )
                Window_global.saveInfo()
            
    def setImageBase(self, imageBase):
        self.imageBase = imageBase
        
        



class Tab( QTabWidget ):
    
    def __init__(self, *args, **kwargs ):
        super( Tab, self ).__init__( *args, **kwargs )
        self.installEventFilter(self)

    def addTab(self, label ):
        imageBase = ImageBase()
        textField = FilePathLine()
        textField.setImageBase( imageBase )
        button = QPushButton("Close Tab")
        
        layoutWidget = QWidget()
        vLayout = QVBoxLayout(layoutWidget)
        vLayout.setContentsMargins(5,5,5,5)
        
        vLayout.addWidget( textField )
        vLayout.addWidget( imageBase )
        vLayout.addWidget( button )
        
        super( Tab, self ).addTab( layoutWidget, label )
        self.setCurrentIndex( self.count() -1 )
        
        def removeThisTab( button ):
            targetWidget = button.parent().parent()
            tabWidget = targetWidget.parent()
            index = tabWidget.indexOf( button.parent() )
            tabWidget.removeTab( index )
            
        button.clicked.connect( partial( removeThisTab, button ) )


    def getChildrenInfo(self):
        
        targetChildren = []
        
        for i in range( self.count() ):
            widgets = self.widget(i).children()
            targetWidgets = {}
            targetWidgets.update( {"tabText": self.tabText(i) })
            for widget in widgets:
                if widget.__class__ == FilePathLine:
                    targetWidgets.update( {"imagePath": widget.text()} )
                elif widget.__class__ == ImageBase:
                    targetWidgets.update( {"imagePosition": [widget.transInfo.x, widget.transInfo.y, widget.transInfo.scale, widget.transInfo.rotValue, widget.transInfo.scaleMultX ]  })
            targetChildren.append( targetWidgets )
        return targetChildren



class AddTabButton( QPushButton ):
    
    def __init__(self, *args, **kwargs ):
        QPushButton.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.clickedX = 0
        self.clickedY= 0
    
    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.clickedX = event.x()
            self.clickedY = event.y()



class Window( QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowFlags(QtCore.Qt.Drawer)
    
        self.layoutWidget = QWidget()
        self.setCentralWidget( self.layoutWidget )
        
        self.layout = QVBoxLayout( self.layoutWidget )
        self.layout.setContentsMargins( 5,5,5,5 )
        
        hLayoutWidget = QWidget()
        self.addTabButton = AddTabButton("Add Tab")
        self.duplicateButton = AddTabButton("Duplicate Tab")
        hLayout = QHBoxLayout(hLayoutWidget)
        hLayout.setContentsMargins( 5,5,5,5 )
        hLayout.addWidget( self.addTabButton )
        hLayout.addWidget( self.duplicateButton )
        
        self.tabWidget = Tab()
        
        self.layout.addWidget( hLayoutWidget )
        self.layout.addWidget( self.tabWidget )
        
        self.addTabButton.clicked.connect( self.promptDialog )
        self.duplicateButton.clicked.connect( self.duplicateDialog )
    
    
    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            Window_global.saveInfo()


    def promptDialog(self, evt=0 ):
        
        mainPos    = self.pos()
        
        objectName = Window_global.objectName + "_dialog"
        if cmds.window( objectName, ex=1 ):
            cmds.deleteUI( objectName )
        
        dialog = QMainWindow( self )
        dialog.setWindowFlags( QtCore.Qt.Dialog )
        dialog.setObjectName( objectName )
        dialog.resize( 200, 100 )
        dialog.move( self.addTabButton.clickedX + mainPos.x()+10, self.addTabButton.clickedY + mainPos.y() + 40 )
        dialog.show()
        
        vWidget = QWidget( dialog )
        vLayout = QVBoxLayout( vWidget )
        dialog.setCentralWidget( vWidget )
        
        hEditLayout = QHBoxLayout()
        hButtonLayout = QHBoxLayout()
        
        vLayout.addLayout( hEditLayout )
        vLayout.addLayout( hButtonLayout )
        
        textWidget = QLabel( "Tab Name : " )
        editWidget = QLineEdit()
        
        hEditLayout.addWidget( textWidget )
        hEditLayout.addWidget( editWidget )
        
        okButtonWidget = QPushButton("OK")
        cancelButtonWidget = QPushButton( "Cancel" )
        
        hButtonLayout.addWidget( okButtonWidget )
        hButtonLayout.addWidget( cancelButtonWidget )
        
        def addTabFunc( evt=0 ):
            self.tabWidget.addTab( editWidget.text() )
            dialog.close()
        
        cancelButtonWidget.clicked.connect( dialog.close )
        okButtonWidget.clicked.connect( addTabFunc )
        editWidget.returnPressed.connect( addTabFunc )


    def duplicateDialog(self, evt=0):
        
        import copy
        
        index = self.tabWidget.currentIndex()
        widgets = self.tabWidget.widget(index).children()
        
        tabText = self.tabWidget.tabText(index)
        imagePath = ''
        transInfo = None
        
        for widget in widgets:
            if widget.__class__ == FilePathLine:
                imagePath = widget.text()
            elif widget.__class__ == ImageBase:
                transInfo = widget.transInfo
        
        self.tabWidget.addTab( tabText )
        
        newIndex = self.tabWidget.currentIndex()
        newWidgets = self.tabWidget.widget(newIndex).children() 
        
        for widget in newWidgets:
            if widget.__class__ == FilePathLine:
                widget.setText( imagePath )
            elif widget.__class__ == ImageBase:
                widget.transInfo = copy.copy(transInfo)
                widget.loadImage( imagePath )
                widget.resize()



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.loadInfo()
    Window_global.mainGui.show()



if __name__ == '__main__':
    show()