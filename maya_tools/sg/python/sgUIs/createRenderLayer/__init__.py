#coding=utf8

from maya import OpenMayaUI, cmds
from PySide import QtGui, QtCore
import shiboken
import os, json
from PySide.QtGui import QVBoxLayout
from functools import partial


class Commands:
    
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
        Commands.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f )
        f.close()




class LineEditEventFilter( QtCore.QObject ):
    
    def __init__(self,*args, **kwargs ):
        QtCore.QObject.__init__( self, *args, **kwargs )


    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.KeyPress ]:
            event.key()
        
        





class TabWidget( QtGui.QTabWidget ):
    
    def __init__(self, *args, **kwargs ):
        QtGui.QTabWidget.__init__( self, *args, **kwargs )
        self.lineEditEventFilter = LineEditEventFilter()
        self.lineLayouts = []


    
    def deleteTab(self):
        
        dialog = QtGui.QDialog( self )
        dialog.setWindowTitle( "Remove Tab" )
        dialog.resize( 300, 50 )
        
        mainLayout = QtGui.QVBoxLayout(dialog)
        
        description = QtGui.QLabel( "'%s' 탭을 삭제하시겠 습니까?".decode('utf-8') % self.tabText( self.currentIndex() ) )
        layoutButtons = QtGui.QHBoxLayout()
        buttonDelete = QtGui.QPushButton( "지우기".decode('utf-8') )
        buttonCancel = QtGui.QPushButton( "취소".decode('utf-8') )
        
        layoutButtons.addWidget( buttonDelete )
        layoutButtons.addWidget( buttonCancel )
        
        mainLayout.addWidget( description )
        mainLayout.addLayout( layoutButtons )
        
        dialog.show()
        
        def cmd_delete():
            self.removeTab( self.indexOf( self.currentWidget() ) )
            dialog.close()
        
        def cmd_cancel():
            dialog.close()
            
        QtCore.QObject.connect( buttonDelete, QtCore.SIGNAL('clicked()'), cmd_delete )
        QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL('clicked()'), cmd_cancel )
    


    def addTab(self, name ):
        
        newWidget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout( newWidget )
        labelEmpty = QtGui.QLabel(); labelEmpty.setMinimumHeight(5)
        buttonDelete = QtGui.QPushButton( "Delete Tab" )
        layout.addWidget( labelEmpty )
        layout.addWidget( buttonDelete )
        QtGui.QTabWidget.addTab( self, newWidget, name )
        
        QtCore.QObject.connect( buttonDelete, QtCore.SIGNAL( 'clicked()' ), self.deleteTab )
    
    
    def currentCount(self):
        
        cuWidget = self.currentWidget()
        if not cuWidget: return 0
        return cuWidget.count()
    
    
    
    def addLine(self):
        
        baseLayout = self.currentWidget().children()[0]
        
        lineLayout = QtGui.QHBoxLayout()
        lineLayout.setContentsMargins(1,1,1,1)
        checkBox = QtGui.QCheckBox(); checkBox.setChecked(True); checkBox.setContentsMargins(1,1,1,1)
        lineEdit = QtGui.QLineEdit(); lineEdit.setContentsMargins(1,1,1,1)
        lineEdit.installEventFilter( self.lineEditEventFilter )
        button = QtGui.QPushButton( " - " ); button.setContentsMargins(1,1,1,1)
        lineLayout.addWidget( checkBox )
        lineLayout.addWidget( lineEdit )
        lineLayout.addWidget( button )
        baseLayout.insertLayout( baseLayout.count()-2, lineLayout )
        
        QtCore.QObject.connect( button, QtCore.SIGNAL( "clicked()" ), partial( self.removeLine, lineLayout ) )
        self.lineLayouts.append( lineLayout )
    
    
    
    def getFromCurrent(self):
        
        pass
    
    
    def removeAll(self):
        for lineLayout in [ lineLayout for lineLayout in self.lineLayouts]:
            self.removeLine( lineLayout )
    
    
    def removeLine(self, lineLayout ):
        
        for i in range( lineLayout.count() ):
            targetWidget = lineLayout.takeAt( 0 ).widget()
            targetWidget.setParent(None)
        lineLayout.setParent( None )
        self.lineLayouts.remove( lineLayout )
        
    




class Window( QtGui.QMainWindow ):
    
    objectName = 'ui_createRenderLayer'
    title = "UI - Create Render Layer"
    defaultWidth = 400
    defaultHeight = 50
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/ui_createRenderLayer"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        mainWidget = QtGui.QWidget(); self.setCentralWidget( mainWidget )
        mainLayout = QtGui.QVBoxLayout( mainWidget )
        
        addButtonsLayout = QtGui.QHBoxLayout()
        buttonAddTab = QtGui.QPushButton( 'Add Tab' )
        buttonAddLine = QtGui.QPushButton( 'Add Line' )
        addButtonsLayout.addWidget( buttonAddTab )
        addButtonsLayout.addWidget( buttonAddLine )
        
        tabWidget = TabWidget()
        self.tabWidget = tabWidget
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonCreate = QtGui.QPushButton( "Create" )
        buttonClose = QtGui.QPushButton( "Close" )
        buttonLayout.addWidget( buttonCreate )
        buttonLayout.addWidget( buttonClose )

        mainLayout.addLayout( addButtonsLayout )
        mainLayout.addWidget( tabWidget )
        mainLayout.addLayout( buttonLayout )
    
        QtCore.QObject.connect( buttonAddTab, QtCore.SIGNAL( 'clicked()' ), partial( self.addTab ) )
        QtCore.QObject.connect( buttonAddLine, QtCore.SIGNAL( "clicked()" ), partial( tabWidget.addLine ) )
        QtCore.QObject.connect( buttonCreate, QtCore.SIGNAL( "clicked()" ), self.cmd_create )
        QtCore.QObject.connect( buttonClose, QtCore.SIGNAL( "clicked()" ), self.cmd_close )
    
    
    
    def addTab(self):
        
        dialog = QtGui.QDialog( self )
        dialog.setWindowTitle( 'Add Tab' )
        dialog.resize( 300, 50 )
        
        mainLayout = QtGui.QVBoxLayout( dialog )
        
        tabNameLayout = QtGui.QHBoxLayout()
        labelTabName = QtGui.QLabel( 'Tab Name : ' )
        lineEditTabName = QtGui.QLineEdit()
        tabNameLayout.addWidget( labelTabName )
        tabNameLayout.addWidget( lineEditTabName )
        
        buttonsLayout = QtGui.QHBoxLayout()
        buttonCreate = QtGui.QPushButton( "Create" )
        buttonCancel  = QtGui.QPushButton( "Cancel")
        buttonsLayout.addWidget( buttonCreate )
        buttonsLayout.addWidget( buttonCancel )
        
        mainLayout.addLayout( tabNameLayout )
        mainLayout.addLayout( buttonsLayout )
        
        dialog.show()

        def cmd_create():            
            tabName = lineEditTabName.text()
            if not tabName:
                msgbox = QtGui.QMessageBox( self )
                msgbox.setText( "이름을 지정해주세요".decode( 'utf-8' ) )
                msgbox.exec_()
                return

            self.tabWidget.addTab( tabName )
            dialog.close()
        
        def cmd_cancel():
            dialog.close()
        
        QtCore.QObject.connect( lineEditTabName, QtCore.SIGNAL( 'returnPressed()' ), cmd_create )
        QtCore.QObject.connect( buttonCreate, QtCore.SIGNAL( 'clicked()' ), cmd_create )
        QtCore.QObject.connect( buttonCancel, QtCore.SIGNAL( 'clicked()' ), cmd_cancel )
            
    
    
    
    def cmd_create(self):
        self.tabWidget.removeAll()
        pass
    
    
    
    def cmd_close(self):
        cmds.deleteUI( Window.objectName )
        

    
    
    def show( self, *args, **kwargs):
        
        self.loadUIInfo()
        QtGui.QMainWindow.show( self, *args, **kwargs )
    


    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            self.saveUIInfo()
    
    
    def saveUIInfo( self ):
        Commands.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        mainWindowDict = {}
        mainWindowDict['position'] = [ self.x(), self.y() ]
        mainWindowDict['size'] = [ self.width(), self.height() ]
        
        data[ 'mainWindow' ] = mainWindowDict
        
        f = open( Window.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        


    def loadUIInfo( self ):
        
        Commands.makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            self.resize( self.defaultWidth, self.defaultHeight )
            return
        try:
            posX, posY = data['mainWindow']['position']
            width, height = data['mainWindow']['size']
        except:
            return
        desktop = QtGui.QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        self.move( posX, posY )
        self.resize( width, height )
        


def show():
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    win = Window( mayawin )
    win.show()
