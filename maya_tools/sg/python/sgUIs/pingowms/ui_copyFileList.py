#coding=utf8

import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken as shiboken
import os, sys
import json




class ListWidgetCopyInfo( QtGui.QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QTreeWidget.__init__( self, *args, **kwargs )
        self.setColumnCount(2)
        headerItem = self.headerItem()
        headerItem.setText( 0, '기존경로'.decode('utf-8') )
        headerItem.setText( 1, '복사경로'.decode('utf-8') )




class Window( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms_copyfileList'
    title = "Pingo WMS CopyFileList"
    defaultWidth = 550
    defaultHeight = 300
    
    mayawin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    mainui = QtGui.QMainWindow()

    def __init__(self, *args, **kwargs ):
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )
        
        baseWidget = QtGui.QWidget()
        self.setCentralWidget( baseWidget )
        
        vLayout = QtGui.QVBoxLayout( baseWidget )
        
        labelInfo = QtGui.QLabel( "해당 파일들이 복사 됩니다.".decode( 'utf-8' ) )
        
        listCopyInfo = ListWidgetCopyInfo()
        
        vLayout.addWidget( labelInfo )
        vLayout.addWidget( listCopyInfo )



def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    Window.mainui = Window( Window.mayawin )
    Window.mainui.show()