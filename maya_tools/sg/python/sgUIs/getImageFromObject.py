import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial
from test.test_imageop import getimage



def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
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
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    objectName = "sgui_getImageFromObject"
    title = "Get Image From Object"
    width = 300
    height = 300
    
    infoPath = cmds.about(pd=True) + "/sg/getImageFromObject/uiInfo.txt"
    infoPath2 = cmds.about( pd=True ) + '/sg/getImageFromObject/uiInfo2.txt'
    makeFile( infoPath )
    makeFile( infoPath2 )
    
    mainGui = QtGui.QMainWindow()
    listItems = []
    
    lineEditObjectName = 'sgui_getImageFromObject_lineEdit'
    listWidgetObjectName = 'sgui_getImageFromObject_listWidget'
    tabObjectName = 'sgui_getImageFromObject_tab'
    
    @staticmethod
    def saveInfo2(filePath=None):
        if not filePath:
            filePath = Window_global.infoPath2
        
        leftSplitterSize = Window_global.leftSplitter.sizes()
        splitterSize = Window_global.splitter.sizes()
        numTab = Window_global.tabWidget.count()
        lineEditTextList = []
        for i in range( numTab ):
            tabElement = Window_global.tabWidget.widget( i )
            targetLineEdit = tabElement.findChild( QtGui.QLineEdit, Window_global.lineEditObjectName )
            lineEditTextList.append( targetLineEdit.text() )
        
        f = open( filePath, 'w' )
        json.dump( [ leftSplitterSize, splitterSize, lineEditTextList ], f, True, False, False )
        f.close()
    
    @staticmethod
    def loadInfo2( filePath=None ):
        if not filePath:
            filePath = Window_global.infoPath2
        
        f = open( filePath, 'r' )
        data = json.load( f )
        f.close()
        
        leftSplitterSize    = data[0]
        splitterSize        = data[1]
        lineEditTextList    = data[2]
        
        Window_global.leftSplitter.setSizes( leftSplitterSize )
        Window_global.splitter.setSizes( splitterSize )
        
        for i in range( len( lineEditTextList ) ):
            Window_global.tabWidget.addTab( 'tab' )
            addedLineEdit = Window_global.tabWidget.widget(i).findChild( QtGui.QLineEdit, Window_global.lineEditObjectName )
            addedLineEdit.setText( lineEditTextList[i] )
            Window_global.tabWidget.widget(i)
            Functions.updateList()
        
    

    @staticmethod
    def saveInfo( filePath = None ):
        
        if not filePath:
            filePath = Window_global.infoPath
        
        posX = Window_global.mainGui.pos().x()
        posY = Window_global.mainGui.pos().y()
        width  = Window_global.mainGui.width()
        height = Window_global.mainGui.height()
        
        f = open( filePath, "w" )
        json.dump( [posX, posY, width, height ], f, True, False, False )
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
            
            desktop = QtGui.QApplication.desktop()
            desktopWidth = desktop.width()
            desktopHeight = desktop.height()
            if posX + width > desktopWidth: posX = desktopWidth - width
            if posY + height > desktopWidth: posY = desktopHeight - height
            if posX < 0 : posX = 0
            if posY < 0 : posY = 0
            
            Window_global.mainGui.move( posX, posY )
        except:
            pass




class ImageBaseTranslateInfo():
    
    def __init__(self ):
        
        self.setDefault()
    
    
    def setDefault(self):
        
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
            rect = QtGui.QApplication.desktop().screenGeometry();
            height = rect.height()/4
            self.scale = self.bScale * (2**(float(moveX)/height))
            scaledValue = self.scale/  self.bScale
            
            self.x = (self.bx - self.pressX) * scaledValue + self.pressX
            self.y = (self.by - self.pressY) * scaledValue + self.pressY



class ImageBase(QtGui.QLabel):

    def __init__(self, *args, **kwargs):
        
        self.transInfo = ImageBaseTranslateInfo()
        
        super(ImageBase, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        
        self.image            = QtGui.QImage()
        self.pixmap = QtGui.QPixmap()
        self.label = QtGui.QLabel(self)
        self.imagePath = ""
        self.aspect = 1
        
    
    def loadImage(self, filePath ):
        
        if self.imagePath == filePath: return None
        self.imagePath = filePath
        
        self.aspect = 1
        if self.image.load(filePath): pass
        self.transInfo.setDefault()

        widgetSize = self.parentWidget().sizes()[1]
        imageWidth = self.image.width()
        
        self.transInfo.scale = widgetSize / float( imageWidth )
        self.resize()
        

    def resize(self):
        
        trValue = QtGui.QTransform().scale( self.transInfo.scaleX(), self.transInfo.scaleY() )
        trValue *= QtGui.QTransform().rotate( self.transInfo.rotValue )
        imageTransformed = self.image.transformed(trValue)
        
        imageWidth  = imageTransformed.width()
        imageHeight = imageTransformed.height()
        
        self.pixmap = QtGui.QPixmap.fromImage( imageTransformed )
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





class Functions:
    
    @staticmethod
    def currentLineEdit():
        currentTabWidget = Window_global.tabWidget.widget( Window_global.tabWidget.currentIndex() )
        return currentTabWidget.findChild( QtGui.QLineEdit, Window_global.lineEditObjectName )
    
    @staticmethod
    def currentTextList():
        currentTabWidget = Window_global.tabWidget.widget( Window_global.tabWidget.currentIndex() )
        return currentTabWidget.findChild( QtGui.QListWidget, Window_global.listWidgetObjectName )
    
    
    @staticmethod
    def setFolder( evt=0 ):
        result = cmds.fileDialog2( fileMode=2, cc='CANCEL', okc='SET' )
        if not result: return None
        Functions.currentLineEdit().setText( result[0] )
        Functions.updateList()
        try:Window_global.saveInfo2()
        except:pass
        
    
    @staticmethod
    def updateList( evt=0 ):
        
        targetExtensions = ['jpg', 'png', 'tga', 'exr']
        
        listWidget = Functions.currentTextList()
        lineEdit   = Functions.currentLineEdit()
        
        folderName = lineEdit.text()
        
        if os.path.exists( folderName ):
            folderName = folderName.replace( '\\', '/' )
            lastFolderName = folderName.split( '/' )[-1]
            Window_global.tabWidget.setTabText( Window_global.tabWidget.currentIndex(), lastFolderName )
        
        for i in range( Functions.currentTextList().count() ):
            listWidget.takeItem(0)
        
        for root, dirs, names in os.walk( folderName ):
            for name in names:
                extension = name.split( '.' )[-1]
                if not extension in targetExtensions: continue
                listWidget.addItem( name )
            break
        
            
    
    @staticmethod
    def loadImage( evt=0 ):
        folderName = Functions.currentLineEdit().text()
        try:
            selItem = Functions.currentTextList().currentItem().text()
            if os.path.isfile( folderName + '/' + selItem ):
                Window_global.imageBase.loadImage( folderName + '/' + selItem )
        except:
            pass
    
    
    @staticmethod
    def getImage( evt=0 ):
        pass
    
    
    @staticmethod
    def openFileBrowser( path='', *args ):
    
        if not os.path.isfile( path ) and not os.path.isdir( path ):
            cmds.warning( 'Path is not Exists' )
        
        path = path.replace( '\\', '/' )
        if os.path.isfile( path ):
            path = '/'.join( path.split( '/' )[:-1] )
            
        os.startfile( path )
    
    
    @staticmethod
    def updatePathPopupMenu( addCommand=None ):

        lineEdit  = Functions.currentLineEdit()
        popupMenu = Functions.currentTextList()
        
        cmds.popupMenu( popupMenu, e=1, dai=1 )
        cmds.setParent( popupMenu, menu=1 )
        path = lineEdit.text()
        cmds.menuItem( l='Open File Browser', c=partial( Functions.openFileBrowser, path ) )
        cmds.menuItem( d=1 )
        
        def backToUpfolder( path, *args ):
            path = path.replace( '\\', '/' )
            path = '/'.join( path.split( '/' )[:-1] )
            lineEdit.setText( path )
            Functions.updatePathPopupMenu( addCommand )
            
        if os.path.isfile(path) or os.path.isdir(path):
            splitPath = path.replace( '\\', '/' ).split( '/' )
            if splitPath and splitPath[-1] != '':
                cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
        cmds.menuItem( d=1 )
        
        path = path.replace( '\\', '/' )
        if os.path.isfile(path):
            path = '/'.join( path.split( '/')[:-1] )
        
        def updateTextField( path, *args ):
            lineEdit.setText( path )
            
            if( addCommand != None ): addCommand()
        
        for root, dirs, names in os.walk( path ):
            dirs.sort()
            for dir in dirs:
                cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
            '''
            names.sort()
            for name in names:
                extension = name.split( '.' )
                if len( extension ) == 1: continue
                extension = extension[1]
                if not extension.lower() in targetExtensions:continue
                cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )'''
            break
        
        Functions.updateList()
    
    
class lineEditEventFilter( QtCore.QObject ):
    
    def __init__(self):
        QtCore.QObject.__init__( self )
    
    def eventFilter( self, *args, **kwarngs ):
        event = args[1]
        if event.type() == QtCore.QEvent.KeyRelease:
            path = Functions.currentLineEdit().text()
            if os.path.exists( path ):
                try:Window_global.saveInfo2()
                except:pass



class Tab( QtGui.QTabWidget ):
    
    def __init__(self, *args, **kwargs ):
        super( Tab, self ).__init__( *args, **kwargs )
        self.installEventFilter(self)


    def addTab(self, label ):
        
        layoutWidget = QtGui.QWidget()
        vLayout = QtGui.QVBoxLayout(layoutWidget)
        vLayout.setContentsMargins(5,5,5,5)
        
        setFolderLayout = QtGui.QHBoxLayout()
        listWidget = QtGui.QListWidget()
        getImageButton = QtGui.QPushButton( 'Get Image' )
        vLayout.addLayout( setFolderLayout )
        vLayout.addWidget( listWidget )
        vLayout.addWidget( getImageButton )
        
        lineEdit = QtGui.QLineEdit()
        setFolderButton = QtGui.QPushButton( 'Set Folder' )
        
        setFolderLayout.addWidget( lineEdit )
        setFolderLayout.addWidget( setFolderButton )
        
        QtCore.QObject.connect( setFolderButton, QtCore.SIGNAL( 'clicked()' ),  Functions.setFolder )
        QtCore.QObject.connect( listWidget, QtCore.SIGNAL( 'itemSelectionChanged()' ),  Functions.loadImage )
        QtCore.QObject.connect( getImageButton,  QtCore.SIGNAL( 'clicked()' ),  Functions.getImage  )
        
        listWidget.setObjectName( Window_global.listWidgetObjectName )
        
        lineEdit.setContextMenuPolicy( QtCore.Qt.NoContextMenu )
        lineEdit.setObjectName( Window_global.lineEditObjectName )
        Window_global.popupMenu = cmds.popupMenu( p=lineEdit.objectName() )
        
        super( Tab, self ).addTab( layoutWidget, label )
        
        self.lineEditEvnetFilter = lineEditEventFilter()
        lineEdit.installEventFilter( self.lineEditEvnetFilter )
    
        
        
        


class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        #self.setWindowFlags( QtCore.Qt.Drawer )
        self.setWindowTitle( Window_global.title )
        
        splitter = QtGui.QSplitter()
        self.setCentralWidget( splitter )
        
        leftSplitter = QtGui.QSplitter(); leftSplitter.setOrientation( QtCore.Qt.Vertical )
        imageBase = ImageBase()
        splitter.addWidget( leftSplitter )
        splitter.addWidget( imageBase )
        
        widgetSelArea = QtGui.QWidget()
        layoutSelArea = QtGui.QVBoxLayout(widgetSelArea)
        widgetPathArea = QtGui.QWidget()
        layoutPathArea = QtGui.QVBoxLayout( widgetPathArea )
        leftSplitter.addWidget( widgetSelArea )
        leftSplitter.addWidget( widgetPathArea )
        
        labelSelTextList = QtGui.QLabel( 'Images from Selection' )
        selTextList = QtGui.QListWidget()
        layoutSelArea.addWidget( labelSelTextList )
        layoutSelArea.addWidget( selTextList )
        
        tab = Tab()
        tab.setObjectName( Window_global.tabObjectName )
        layoutPathArea.addWidget( tab )
        self.tabWidget = tab
        cmds.popupMenu( p=tab.objectName() )
        cmds.menuItem( l='Add Tab', c= self.addTab )
        cmds.menuItem( l='Remove Tab', c= self.removeTab )
        
        Window_global.imageBase  = imageBase
        Window_global.splitter   = splitter
        Window_global.leftSplitter = leftSplitter
        Window_global.tabWidget  = tab
        
        splitter.setSizes( [100,100] )
        leftSplitter.setSizes( [100,100] )
        
        Window_global.loadInfo()
        try:Window_global.loadInfo2()
        except:pass
    
    
    def addTab(self, evt=0 ):
        self.tabWidget.addTab( 'newTab' )


    def removeTab(self, evt=0):
        self.tabWidget.removeTab( self.tabWidget.currentIndex() )
        

    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() in [QtCore.QEvent.LayoutRequest,QtCore.QEvent.Move,QtCore.QEvent.Resize] :
            Window_global.saveInfo()
            try:Window_global.saveInfo2()
            except:pass



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.loadInfo()
    Window_global.mainGui.show()

