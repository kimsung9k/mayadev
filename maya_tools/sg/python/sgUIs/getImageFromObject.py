import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json
from functools import partial



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
    getImageObjectName = 'sgui_getImageFromObject_getButton'
    removeImageObjectName = 'sgui_getImageFromObject_removeButton'
    tabObjectName = 'sgui_getImageFromObject_tab'


    @staticmethod
    def saveInfo2(filePath=None):
        if not filePath:
            filePath = Window_global.infoPath2
        
        verticalSplitterSize = Window_global.verticalSplitter.sizes()
        horizonSplitter1Size = Window_global.horizonSplitter1.sizes()
        horizonSplitter2Size = Window_global.horizonSplitter2.sizes()
        numTab = Window_global.tabWidget.count()
        lineEditTextList = []
        selIndex = Window_global.tabWidget.currentIndex()
        for i in range( numTab ):
            tabElement = Window_global.tabWidget.widget( i )
            targetLineEdit = tabElement.findChild( QtGui.QLineEdit, Window_global.lineEditObjectName )
            lineEditTextList.append( targetLineEdit.text() )
        
        f = open( filePath, 'w' )
        json.dump( [ verticalSplitterSize, horizonSplitter1Size, horizonSplitter2Size, lineEditTextList, selIndex ], f, True, False, False )
        f.close()


    @staticmethod
    def loadInfo2( filePath=None ):
        if not filePath:
            filePath = Window_global.infoPath2
        
        f = open( filePath, 'r' )
        data = json.load( f )
        f.close()
        
        verticalSplitterSize = data[0]
        horizonSplitter1Size = data[1]
        horizonSplitter2Size = data[2]
        lineEditTextList    = data[3]
        currentIndex        = data[4]
        
        Window_global.verticalSplitter.setSizes( verticalSplitterSize )
        Window_global.horizonSplitter1.setSizes( horizonSplitter1Size )
        Window_global.horizonSplitter2.setSizes( horizonSplitter2Size )
        
        for i in range( Window_global.tabWidget.count() ):
            Window_global.tabWidget.removeTab( i )
        
        for i in range( len( lineEditTextList ) ):
            Window_global.tabWidget.addTab( 'newTab' )
            addedLineEdit = Window_global.tabWidget.widget(i).findChild( QtGui.QLineEdit, Window_global.lineEditObjectName )
            addedLineEdit.setText( lineEditTextList[i] )
            Window_global.tabWidget.setCurrentIndex( i )
            Functions.updateList()  
        Window_global.tabWidget.setCurrentIndex( currentIndex )
    

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
        self.imageClean = True
    
    
    def clearImage(self):
        
        self.label.clear()
        self.imageClean = True

    
    
    def loadImage(self, filePath ):
        
        self.imageClean = False
        if self.imagePath == filePath: return None
        self.imagePath = filePath
        
        self.aspect = 1
        if self.image.load(filePath): pass
        self.transInfo.setDefault()

        widgetSize = min( self.parentWidget().width(), self.parentWidget().height()  ) * 0.9
        imageWidth = self.image.width()
        
        self.transInfo.scale = widgetSize / float( imageWidth )
        self.resize()
        

    def resize(self):
        
        if self.imageClean: return None
        
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
        self.label.paintEvent(QtGui.QPaintEvent(QtCore.QRect( 0,0,self.width(), self.height() )))
        
        
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
    def updateSelTextureList( evt=0 ):
        
        import pymel.core
        for i in range( Window_global.selTextureList.count() ):
            Window_global.selTextureList.takeItem(0)
        
        sels = pymel.core.ls( sl=1 )
        Window_global.imageBaseSelArea.clearImage()
        
        textureList = []
        for sel in sels:
            try:
                sel.getShape()
            except:
                continue
            shadingGroups = sel.getShape().listConnections( type='shadingEngine' )
            for shadingGroup in shadingGroups:
                hists = shadingGroup.history()
                if not hists: continue
                for hist in hists:
                    if hist.type() != 'file': continue
                    fileTextureName = hist.fileTextureName.get()
                    if not os.path.exists( fileTextureName ): continue
                    if fileTextureName in textureList: continue
                    textureList.append( fileTextureName )
        
        for textureName in textureList:
            Window_global.selTextureList.addItem( textureName )
        
            
    
    @staticmethod
    def loadImagePathArea( evt=0 ):
        
        selItems = Functions.currentTextList().selectedItems()
        if selItems:
            Window_global.removeImageButton.setEnabled( True )
        else:
            Window_global.removeImageButton.setEnabled( False )
        
        folderName = Functions.currentLineEdit().text()
        try:
            selItem = Functions.currentTextList().currentItem().text()
            if os.path.isfile( folderName + '/' + selItem ):
                Window_global.imageBasePathArea.loadImage( folderName + '/' + selItem )
        except:
            pass
    
    
    
    @staticmethod
    def loadImageSelArea( evt=0 ):
        
        selItems = Window_global.selTextureList.selectedItems()
        if selItems:
            Window_global.getImageButton.setEnabled( True )
        else:
            Window_global.getImageButton.setEnabled( False )
        
        try:
            selItem = Window_global.selTextureList.currentItem().text()
            if os.path.isfile( selItem ):
                Window_global.imageBaseSelArea.loadImage( selItem )
        except:
            pass
    
    
    @staticmethod
    def getImage( evt=0 ):
        import shutil
        folderName = Functions.currentLineEdit().text()
        selItems = Window_global.selTextureList.selectedItems()

        existsPaths = []        
        sourcePaths = []
        targetPaths = []
        for selItem in selItems:
            srcPath = selItem.text()
            if not os.path.exists( srcPath ): continue
            srcPath = srcPath.replace( '\\', '/' )
            targetPath = folderName + '/' + srcPath.split( '/' )[-1]
            
            if srcPath in sourcePaths: continue
            
            sourcePaths.append( srcPath )
            targetPaths.append( targetPath )
            if os.path.exists( targetPath ):
                existsPaths.append( targetPath )

        if existsPaths:
            warnString = ''
            for existPath in existsPaths:
                warnString += existPath + ',\n'
            warnString += 'Aleady Exists.'
            warnString += 'Do you want to replace it?'
            result = cmds.confirmDialog( title='Confirm', message=warnString, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if result != 'Yes': return None

        for i in range( len( sourcePaths ) ):
            shutil.copy2( sourcePaths[i], targetPaths[i] )
        
        Functions.updateList()


    @staticmethod
    def removeImage( evt=0 ):
        
        folderName = Functions.currentLineEdit().text()
        selItems = Functions.currentTextList().selectedItems()
        
        delTargets = []
        
        for selItem in selItems:
            fileName = selItem.text()
            filePath = folderName + '/' + fileName
            if not os.path.exists( filePath ) : continue
            delTargets.append( filePath )
        
        if not delTargets: return None
        
        warnString = ''
        for delTarget in delTargets:
            warnString += delTarget + ',\n'
        warnString += 'will be deleted.'
        warnString += 'Are you sure?'
        
        result = cmds.confirmDialog( title='Confirm', message=warnString, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'Yes':
            for delTarget in delTargets:
                os.remove( delTarget )
            
        Functions.updateList()
        
        
    
    
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
        
            
    
    @staticmethod
    def splitterMoved1( *args ):
        sizes = Window_global.horizonSplitter1.sizes()
        Window_global.horizonSplitter2.setSizes( sizes ) 
    
    
    @staticmethod
    def splitterMoved2( *args ):
        sizes = Window_global.horizonSplitter2.sizes()
        Window_global.horizonSplitter1.setSizes( sizes )
    
    
    
    @staticmethod
    def lineEdited( *args ):
        Functions.updateList()
        Window_global.saveInfo2()
    




class SplitterEventFilter( QtCore.QObject ):
    
    def __init__(self):
        QtCore.QObject.__init__( self )
    
    def eventFilter(self, *args, **kwarngs ):
        event = args[1]
        if event.type() == QtCore.QEvent.Paint:
            #Functions.splitterMoved()
            pass




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
        listWidget.setSelectionMode( QtGui.QAbstractItemView.ExtendedSelection )
        vLayout.addLayout( setFolderLayout )
        vLayout.addWidget( listWidget )
        
        lineEdit = QtGui.QLineEdit()
        setFolderButton = QtGui.QPushButton( 'Set Folder' )
        
        setFolderLayout.addWidget( lineEdit )
        setFolderLayout.addWidget( setFolderButton )
        
        QtCore.QObject.connect( setFolderButton, QtCore.SIGNAL( 'clicked()' ),  Functions.setFolder )
        QtCore.QObject.connect( listWidget, QtCore.SIGNAL( 'itemSelectionChanged()' ),  Functions.loadImagePathArea )
        QtCore.QObject.connect( lineEdit, QtCore.SIGNAL( 'textChanged()' ), Functions.lineEdited )
        
        listWidget.setObjectName( Window_global.listWidgetObjectName )
        lineEdit.setContextMenuPolicy( QtCore.Qt.NoContextMenu )
        lineEdit.setObjectName( Window_global.lineEditObjectName )
        
        lineEdit.returnPressed.connect( Functions.lineEdited )
        
        super( Tab, self ).addTab( layoutWidget, label )
    
        
        

class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        #self.setWindowFlags( QtCore.Qt.Drawer )
        self.setWindowTitle( Window_global.title )

        verticalSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.setCentralWidget( verticalSplitter )
        
        horizonSplitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        horizonSplitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        
        verticalSplitter.addWidget( horizonSplitter1 )
        verticalSplitter.addWidget( horizonSplitter2 )
        
        widgetSelArea  = QtGui.QWidget()
        layoutSelArea  = QtGui.QVBoxLayout(widgetSelArea)
        labelSelTextList = QtGui.QLabel( 'Images from Selection' )
        selTextureList = QtGui.QListWidget()
        selTextureList.setSelectionMode( QtGui.QAbstractItemView.ExtendedSelection )
        layoutSelArea.addWidget( labelSelTextList )
        layoutSelArea.addWidget( selTextureList )
        imageBaseSelArea = ImageBase()
        
        horizonSplitter1.addWidget( widgetSelArea )
        horizonSplitter1.addWidget( imageBaseSelArea )        
        
        widgetPathArea = QtGui.QWidget()
        layoutPathArea = QtGui.QVBoxLayout( widgetPathArea )
        layoutAddTab = QtGui.QHBoxLayout()
        removeTabButton = QtGui.QPushButton( 'Remove Tab' )
        addTabButton = QtGui.QPushButton( 'Add Tab' )
        self.tabWidget = Tab()
        buttonLayout = QtGui.QHBoxLayout()
        getImageButton = QtGui.QPushButton( 'Get Image' )
        removeImageButton   = QtGui.QPushButton( 'Remove Image' )
        layoutPathArea.addLayout( layoutAddTab )
        layoutPathArea.addWidget( self.tabWidget )
        layoutPathArea.addLayout( buttonLayout )
        imageBasePathArea = ImageBase()
        layoutAddTab.addWidget( removeTabButton )
        layoutAddTab.addWidget( addTabButton )
        buttonLayout.addWidget( getImageButton )
        buttonLayout.addWidget( removeImageButton )
        
        horizonSplitter2.addWidget( widgetPathArea )
        horizonSplitter2.addWidget( imageBasePathArea )        
        
        Window_global.selTextureList  = selTextureList
        Window_global.imageBaseSelArea = imageBaseSelArea
        Window_global.imageBasePathArea = imageBasePathArea
        Window_global.verticalSplitter = verticalSplitter
        Window_global.horizonSplitter1 = horizonSplitter1
        Window_global.horizonSplitter2 = horizonSplitter2
        Window_global.getImageButton = getImageButton
        Window_global.removeImageButton = removeImageButton
        Window_global.tabWidget = self.tabWidget
        Window_global.tabWidget.addTab( 'newTab' )
        
        verticalSplitter.setSizes( [100,100] )
        horizonSplitter1.setSizes( [100,100] )
        horizonSplitter2.setSizes( [100,100] )
        
        Window_global.loadInfo()
        try:Window_global.loadInfo2()
        except:pass
        Functions.updateSelTextureList()
        
        QtCore.QObject.connect( addTabButton,    QtCore.SIGNAL( 'clicked()' ), self.addTab )
        QtCore.QObject.connect( removeTabButton, QtCore.SIGNAL( 'clicked()' ), self.removeTab )
        QtCore.QObject.connect( Window_global.selTextureList, QtCore.SIGNAL( 'itemSelectionChanged()' ),  Functions.loadImageSelArea )
        QtCore.QObject.connect( Window_global.horizonSplitter1, QtCore.SIGNAL( 'splitterMoved(int,int)' ),  Functions.splitterMoved1 )
        QtCore.QObject.connect( Window_global.horizonSplitter2, QtCore.SIGNAL( 'splitterMoved(int,int)' ),  Functions.splitterMoved2 )
        QtCore.QObject.connect( getImageButton,  QtCore.SIGNAL( 'clicked()' ),  Functions.getImage  )
        QtCore.QObject.connect( removeImageButton,  QtCore.SIGNAL( 'clicked()' ),  Functions.removeImage  )
        
        imageBaseSelArea.clear()
        imageBasePathArea.clear()
        
        getImageButton.setEnabled( False )
        removeImageButton.setEnabled( False )
        
        
    def addTab(self, evt=0 ):
        self.tabWidget.addTab( 'newTab' )
        self.tabWidget.setCurrentIndex( self.tabWidget.count()-1 )


    def removeTab(self, evt=0):
        result = cmds.confirmDialog( title='Confirm', message="Delete the current tab?", button=['Ok', 'Cancel'], defaultButton='Ok', cancelButton='Cancel', dismissString='Cancel' )
        if result != 'Ok': return None
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
    
    cmds.scriptJob( e=['SelectionChanged', Functions.updateSelTextureList ], p=Window_global.mainGui.objectName() )
    
    Window_global.loadInfo()
    Window_global.mainGui.show()

