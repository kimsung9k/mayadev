#coding=utf8


import pymel.core
from __qtImport import *
import maya.OpenMayaUI
import os, json



class Cmds:
    
    @staticmethod
    def makeFolder( pathName ):
        
        if os.path.exists( pathName ):return None
        os.makedirs( pathName )
        return pathName



    @staticmethod
    def makeFile( filePath ):
        
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        Cmds.makeFolder( folder )
        f = open( filePath, "w" )
        f.close()
    


    @staticmethod
    def getFurAttrAndValueList():
        
        furAttrAndValues = []
        for furNode in pymel.core.ls( type='FurDescription' ):
            for attr in furNode.listAttr( w=1 ):
                if attr.type() == 'TdataCompound':
                    if not attr.isArray(): continue
                    if not attr.numElements(): continue
                    for i in range( attr.numElements() ):
                        value = attr[i].get()
                        if not value: continue
                        if type( value ) != unicode: continue
                        furAttrAndValues.append( [attr[i].name(), value] )
        return furAttrAndValues
    
    @staticmethod
    def updateFurAttrWidgetList():
        
        furAttrAndValueList = Cmds.getFurAttrAndValueList()
        Win.currentWin.furAttrListWidget.clear()
        for attr, value in furAttrAndValueList:
            newItem = QTreeWidgetItem( Win.currentWin.furAttrListWidget )
            newItem.setText( 0, attr )
            newItem.setText( 1, value )
            if os.path.exists( value ):
                newItem.setText( 2, "Exists" )
            else:
                newItem.setText( 2, "Not Exists" )
        
        Win.currentWin.furAttrListWidget.resizeColumnToContents( 0 )
        resizedWidth = Win.currentWin.furAttrListWidget.columnWidth(0)
        if resizedWidth > 315:
            resizedWidth = 315
        else:
            resizedWidth += 15
        Win.currentWin.furAttrListWidget.setColumnWidth( 0, resizedWidth )
        
        Win.currentWin.furAttrListWidget.resizeColumnToContents( 1 )
        resizedWidth = Win.currentWin.furAttrListWidget.columnWidth(1)
        if resizedWidth > 515:
            resizedWidth = 515
        else:
            resizedWidth += 15
        Win.currentWin.furAttrListWidget.setColumnWidth( 1, resizedWidth )
    
    
    @staticmethod
    def editPath():
        
        dialog = QDialog( Win.currentWin )
        selItems = Win.currentWin.furAttrListWidget.selectedItems()
        if not selItems: return None
        selItem = selItems[0]
        dialog.setWindowTitle( selItem.text(0) )
        
        layout = QVBoxLayout( dialog )
        lineEdit = QLineEdit(); lineEdit.setText( selItem.text(1) )
        buttonLayout = QHBoxLayout()
        button1 = QPushButton( 'Change' )
        button2 = QPushButton( 'Close' )
        buttonLayout.addWidget( button1 )
        buttonLayout.addWidget( button2 )
        layout.addWidget( lineEdit )
        layout.addLayout( buttonLayout )
        
        dialog.resize( 400,30 )
        dialog.show()
        
        def cmd_change():
            selItems = Win.currentWin.furAttrListWidget.selectedItems()
            if selItems:
                selItem = selItems[0]
                attr = selItem.text( 0 )
                pymel.core.setAttr( attr, lineEdit.text() )
            dialog.close()
            Cmds.updateFurAttrWidgetList()
        
        def cmd_close():
            dialog.close()
            
        button1.clicked.connect( cmd_change )
        button2.clicked.connect( cmd_close )
    
    
    @staticmethod
    def replace():
        
        furAttrAndValueList = Cmds.getFurAttrAndValueList()
        
        srcText = Win.currentWin.replaceStringWidget.srcLineEdit.text()
        dstText = Win.currentWin.replaceStringWidget.dstLineEdit.text()
        
        if not srcText: return None
        
        for attr, value in furAttrAndValueList:
            pymel.core.setAttr( attr, value.replace( srcText, dstText ), type='string' )
        
        Cmds.updateFurAttrWidgetList()
    
    
    @staticmethod
    def setToLocalMapFolder():
        
        import ntpath
        
        furAttrAndValueList = Cmds.getFurAttrAndValueList()
        
        scenePath = cmds.file( q=1, sceneName=1 )
        mapFolder = os.path.dirname( scenePath ) + '/maps'
        
        for attr, value in furAttrAndValueList:
            fileName = ntpath.split( value )[-1]
            pymel.core.setAttr( attr, mapFolder + '/' + fileName, type='string' )
        
        Cmds.updateFurAttrWidgetList()
            
    





class FurAttrListWidget( QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QTreeWidget.__init__( self, *args, **kwargs )
        self.setColumnCount(3)
        headerItem = self.headerItem()
        headerItem.setText( 0, 'Fur Attr'.decode('utf-8') )
        headerItem.setText( 1, 'File Path'.decode('utf-8') )
        headerItem.setText( 2, "Condition".decode( "utf-8" ) )
        
        font = QFont();
        font.setPixelSize(12)
        self.setFont(font)
        
        self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        QtCore.QObject.connect( self, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),  self.loadContextMenu )
    
    
    def loadContextMenu(self):
        
        selItems = self.selectedItems()
        if not selItems: return None
        
        menu = QMenu( self )
        menu.addAction( "경로변경".decode('utf-8'), Cmds.editPath )
        
        pos = QCursor.pos()
        point = QtCore.QPoint( pos.x()+10, pos.y() )
        menu.exec_( point )
        
        


class WidgetReplaceString( QWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QWidget.__init__( self, *args, **kwargs )
        
        layout = QVBoxLayout( self )
        srcLayout = QHBoxLayout()
        dstLayout = QHBoxLayout()
        
        mainDesLabel = QLabel( "Replace Path string All" )
        mainDesLabel.setAlignment( QtCore.Qt.AlignCenter )
        
        srcDesLabel = QLabel( "Source String : ")
        dstDesLabel = QLabel( "Dest String : ")
        srcLineEdit = QLineEdit()
        dstLineEdit = QLineEdit()
        buttonReplace = QPushButton( 'Replace' )
        buttonSetToLocalMapFolder = QPushButton( 'Set to local map folder' )
        
        srcLayout.addWidget( srcDesLabel )
        srcLayout.addWidget( srcLineEdit )
        dstLayout.addWidget( dstDesLabel )
        dstLayout.addWidget( dstLineEdit )
        
        layout.addWidget( buttonSetToLocalMapFolder )
        layout.addWidget( mainDesLabel )
        layout.addLayout( srcLayout )
        layout.addLayout( dstLayout )
        layout.addWidget( buttonReplace )
        
        QtCore.QObject.connect( buttonReplace, QtCore.SIGNAL('clicked()'), Cmds.replace )
        QtCore.QObject.connect( buttonSetToLocalMapFolder, QtCore.SIGNAL('clicked()'), Cmds.setToLocalMapFolder )
        
        self.srcLineEdit = srcLineEdit
        self.dstLineEdit = dstLineEdit
        




class Win(QDialog):

    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    
    objectName = 'ui_pingosceneoptimize_furDescriptionMapEditor'
    title = 'Fur Description map Path Editor'
    defaultWidth = 400
    defaultHeight = 150
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/furDescriptionMapEditor"
    uiInfoPath = infoBaseDir + '/uiInfo.json'

    currentWin = None

    
    def __init__(self, *args, **kwargs ):

        QDialog.__init__( self, *args, **kwargs )
        self.setWindowFlags(QtCore.Qt.Drawer)
        self.installEventFilter( self )
        self.setObjectName( Win.objectName )
        self.setWindowTitle( Win.title )
        
        layout = QVBoxLayout( self )
        
        furAttrListWidget = FurAttrListWidget()
        replaceStringWidget = WidgetReplaceString()

        closeButton = QPushButton( 'Close' )
        
        layout.addWidget( furAttrListWidget )
        layout.addWidget( replaceStringWidget )
        layout.addWidget( closeButton )
        
        self.furAttrListWidget = furAttrListWidget
        self.replaceStringWidget = replaceStringWidget
        
        QtCore.QObject.connect( closeButton, QtCore.SIGNAL('clicked()'), self.close )
    
    
    
    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()


    
    def saveUIInfo( self ):
        
        Cmds.makeFile( Win.uiInfoPath )
        f = open( Win.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        mainWindowDict = {}
        mainWindowDict['position'] = [ self.x(), self.y() ]
        mainWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'mainWindow' ] = mainWindowDict
        
        f = open( Win.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        



    def loadUIInfo( self ):
        
        Cmds.makeFile( Win.uiInfoPath )
        f = open( Win.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            Win.currentWin.resize( self.defaultWidth, self.defaultHeight )
            return
        try:
            posX, posY = data['mainWindow']['position']
            width, height = data['mainWindow']['size']
        except:
            return
        desktop = QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        Win.currentWin.move( posX, posY )
        Win.currentWin.resize( width, height )



def show():
    
    if cmds.window( Win.objectName, ex=1 ):
        cmds.deleteUI( Win.objectName, wnd=1 )
    
    Win.currentWin = Win( Win.mayaWin )
    Cmds.updateFurAttrWidgetList()
    Win.currentWin.loadUIInfo()
    Win.currentWin.show()

