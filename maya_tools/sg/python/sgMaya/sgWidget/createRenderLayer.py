#coding=utf8

from maya import OpenMayaUI, cmds
import os, json
from functools import partial



from maya import cmds

if int( cmds.about( v=1 ) ) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction,\
    QFont, QGridLayout, QProgressBar, QIcon
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider,\
    QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction, QGridLayout, QProgressBar
    
    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform,\
    QPaintEvent, QFont, QIcon




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
        
        





class TabWidget( QTabWidget ):
    
    def __init__(self, *args, **kwargs ):
        QTabWidget.__init__( self, *args, **kwargs )
        self.lineEditEventFilter = LineEditEventFilter()
        self.lineLayouts = []


    
    def deleteTab(self):
        
        dialog = QDialog( self )
        dialog.setWindowTitle( "Remove Tab" )
        dialog.resize( 300, 50 )
        
        mainLayout = QVBoxLayout(dialog)
        
        description = QLabel( "'%s' ���� �����Ͻð� ���ϱ�?".decode('utf-8') % self.tabText( self.currentIndex() ) )
        layoutButtons = QHBoxLayout()
        buttonDelete = QPushButton( "�����".decode('utf-8') )
        buttonCancel = QPushButton( "���".decode('utf-8') )
        
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
        
        newWidget = QWidget()
        layout = QVBoxLayout( newWidget )
        labelEmpty = QLabel(); labelEmpty.setMinimumHeight(5)
        buttonDelete = QPushButton( "Delete Tab" )
        layout.addWidget( labelEmpty )
        layout.addWidget( buttonDelete )
        QTabWidget.addTab( self, newWidget, name )
        
        QtCore.QObject.connect( buttonDelete, QtCore.SIGNAL( 'clicked()' ), self.deleteTab )
    
    
    def currentCount(self):
        
        cuWidget = self.currentWidget()
        if not cuWidget: return 0
        return cuWidget.count()
    
    
    
    def addLine(self):
        
        baseLayout = self.currentWidget().children()[0]
        
        lineLayout = QHBoxLayout()
        lineLayout.setContentsMargins(1,1,1,1)
        checkBox = QCheckBox(); checkBox.setChecked(True); checkBox.setContentsMargins(1,1,1,1)
        lineEdit = QLineEdit(); lineEdit.setContentsMargins(1,1,1,1)
        lineEdit.installEventFilter( self.lineEditEventFilter )
        button = QPushButton( " - " ); button.setContentsMargins(1,1,1,1)
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
        
    




class Window( QMainWindow ):
    
    objectName = 'ui_createRenderLayer'
    title = "UI - Create Render Layer"
    defaultWidth = 400
    defaultHeight = 50
    
    infoBaseDir = cmds.about( pd=1 ) + "/sg/ui_createRenderLayer"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    
    def __init__(self, *args, **kwargs ):
        
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        mainWidget = QWidget(); self.setCentralWidget( mainWidget )
        mainLayout = QVBoxLayout( mainWidget )
        
        addButtonsLayout = QHBoxLayout()
        buttonAddTab = QPushButton( 'Add Tab' )
        buttonAddLine = QPushButton( 'Add Line' )
        addButtonsLayout.addWidget( buttonAddTab )
        addButtonsLayout.addWidget( buttonAddLine )
        
        tabWidget = TabWidget()
        self.tabWidget = tabWidget
        
        buttonLayout = QHBoxLayout()
        buttonCreate = QPushButton( "Create" )
        buttonClose = QPushButton( "Close" )
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
        
        dialog = QDialog( self )
        dialog.setWindowTitle( 'Add Tab' )
        dialog.resize( 300, 50 )
        
        mainLayout = QVBoxLayout( dialog )
        
        tabNameLayout = QHBoxLayout()
        labelTabName = QLabel( 'Tab Name : ' )
        lineEditTabName = QLineEdit()
        tabNameLayout.addWidget( labelTabName )
        tabNameLayout.addWidget( lineEditTabName )
        
        buttonsLayout = QHBoxLayout()
        buttonCreate = QPushButton( "Create" )
        buttonCancel  = QPushButton( "Cancel")
        buttonsLayout.addWidget( buttonCreate )
        buttonsLayout.addWidget( buttonCancel )
        
        mainLayout.addLayout( tabNameLayout )
        mainLayout.addLayout( buttonsLayout )
        
        dialog.show()

        def cmd_create():            
            tabName = lineEditTabName.text()
            if not tabName:
                msgbox = QMessageBox( self )
                msgbox.setText( "�̸��� �������ּ���".decode( 'utf-8' ) )
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
        QMainWindow.show( self, *args, **kwargs )
    


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
        desktop = QApplication.desktop()
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
    
    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    win = Window( mayawin )
    win.show()
    
    
if __name__ == '__main__':
    show()
