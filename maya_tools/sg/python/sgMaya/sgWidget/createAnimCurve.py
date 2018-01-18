import maya.OpenMayaUI
import os
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
    objectName = "sg_Tool_createAnimCurve"
    title = "SG Tool Create AnimCurve"
    width = 300
    height = 10
    
    infoPath = cmds.about(pd=True) + "/sg/sg_toolInfo/createAnimCurve.txt"
    makeFile( infoPath )
    
    mainGui = QMainWindow()




class Commands:
    
    @staticmethod
    def connectCommand( uiInstance ):
        
        sels = cmds.ls( sl=1 )
        selChannels = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
        
        numItems = uiInstance.layout.count()
        animNode = cmds.createNode( 'animCurveUU' )
        
        for i in range( 1, numItems-1 ):
            targetWidget = uiInstance.layout.itemAt( i ).widget()
            
            key = targetWidget.lineEdit_key.text()
            value = targetWidget.lineEdit_value.text()
            
            cmds.setKeyframe( animNode, f=float(key), v=float(value) )
            cmds.keyTangent( animNode, f=(float(key),float(key)), itt='linear', ott = 'linear' )
        
        if sels and selChannels:
            cmds.connectAttr( sels[0] + '.' + selChannels[0], animNode + '.input' )
            addString = ''
            if float(key) > 0:
                addString = 'positive'
            else:
                addString = 'negative'
            animNode = cmds.rename( animNode, selChannels[0] + '_' + addString + '_from_' + sels[0] )
        
        cmds.select( animNode )




class UI_labels( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.text_key = QLabel('Float')
        self.text_value = QLabel('Value')
        
        self.text_key.setAlignment( QtCore.Qt.AlignCenter )
        self.text_value.setAlignment( QtCore.Qt.AlignCenter )
        
        self.layout.addWidget( self.text_key )
        self.layout.addWidget( self.text_value )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass




class UI_attrlist( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.lineEdit_key = QLineEdit()
        self.lineEdit_value = QLineEdit()
        
        self.layout.addWidget( self.lineEdit_key )
        self.layout.addWidget( self.lineEdit_value )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass



class UI_buttons( QWidget ):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.button_connect = QPushButton("Create")
        self.button_addLine = QPushButton("Add Line")
        self.lineEdit_value = QLineEdit()
        self.layout.addWidget( self.button_connect )
        self.layout.addWidget( self.button_addLine )
        
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass
    




class Window( QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowFlags(QtCore.Qt.Drawer)
    
        self.layoutWidget = QWidget()
        self.setCentralWidget( self.layoutWidget )
        
        self.layout = QVBoxLayout( self.layoutWidget )
        self.layout.setContentsMargins( 5,5,5,5 )
        
        self.ui_labels     = UI_labels()
        self.ui_driverAttr1 = UI_attrlist()
        self.ui_driverAttr2 = UI_attrlist()
        self.ui_buttons    = UI_buttons()
        self.layout.addWidget( self.ui_labels )
        self.layout.addWidget( self.ui_driverAttr1 )
        self.layout.addWidget( self.ui_driverAttr2 )
        self.layout.addWidget( self.ui_buttons )
        
        self.ui_driverAttr1.lineEdit_key.setText( '0' )
        self.ui_driverAttr1.lineEdit_value.setText( '0' )
        self.ui_driverAttr2.lineEdit_key.setText( '1' )
        self.ui_driverAttr2.lineEdit_value.setText( '1' )
        
        
        def addLineCommand():
            
            numItems = self.layout.count()
            attrlist = UI_attrlist()
            self.layout.insertWidget( numItems-1, attrlist )
        
        self.ui_buttons.button_connect.clicked.connect( partial( Commands.connectCommand, self ) )
        self.ui_buttons.button_addLine.clicked.connect( addLineCommand )
    
    
    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass



def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()



if __name__ == '__main__':
    show()


