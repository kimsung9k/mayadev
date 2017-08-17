#coding=utf8

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
    
    mayawin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    mainui = QtGui.QMainWindow()
    


class Widget_addProject( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms'
    title = "프로젝트 추가".decode('utf-8')
    defaultWidth= 400
    defaultHeight = 200
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Widget_addProject.title )
        self.resize( Widget_addProject.defaultWidth, Widget_addProject.defaultHeight )

    


class UI_Project( QtGui.QWidget ):
    
    label = "프로젝트 명 : ".decode('utf-8')

    def __init__(self):
        
        QtGui.QWidget.__init__( self )
        self.installEventFilter( self )
        
        hLayout = QtGui.QHBoxLayout( self )
        label = QtGui.QLabel( UI_Project.label )
        comboBox = QtGui.QComboBox()
        button = QtGui.QPushButton( " + " )
        hLayout.addWidget( label )
        hLayout.addWidget( comboBox )
        hLayout.addWidget( button )
        
        self.button = button
        
        




class Window( QtGui.QMainWindow ):
    
    objectName = 'ui_pingowms'
    title = "WMS for Maya Pingo Enter 1.0"
    defaultWidth = 550
    defaultHeight = 300
    
    uiInfoDir = cmds.about( pd=1 ) + '/pingowms'
    uiInfoPath = uiInfoDir + '/uiInfo.json'
    projectListPath = uiInfoDir+ '/projectList.json'
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setObjectName( Window.objectName )
        self.setWindowTitle( Window.title )

        baseWidget = QtGui.QWidget()
        self.setCentralWidget( baseWidget )
        
        vLayout = QtGui.QFormLayout( baseWidget )
        ui_project = UI_Project()
        vLayout.addWidget( ui_project )
        
        ui_project.button.clicked.connect( self.show_addProject )
    
    
    def show_addProject( self ):
        
        self.ui_addProject = Widget_addProject( self )
        self.ui_addProject.show()
    
    
    def eventFilter(self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.Resize or event.type() == QtCore.QEvent.Move:
            self.saveUIInfo()

    @staticmethod
    def loadProjectList():
        makeFile( Window.projectListPath )
        f = open( Window.projectListPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        print data
    
    
    def saveUIInfo( self ):
        makeFile( Window.uiInfoPath )
        f = open( Window.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        
        data['position'] = [ self.x(), self.y() ]
        data['size'] = [ self.width(), self.height() ]
        
        print data
        
        f = open( Window.uiInfoPath, 'w' )
        json.dump( data, f )
        f.close()
        
    
    def loadUIInfo( self ):
        makeFile( self.uiInfoPath )
        f = open( self.uiInfoPath, 'r' )
        try:data = json.load( f )
        except:data = {}
        f.close()
        if not data.items():
            Window_global.mainui.resize( self.defaultWidth, self.defaultHeight )
            return
        
        posX, posY = data['position']
        width, height = data['size']
        
        desktop = QtGui.QApplication.desktop()
        desktopWidth = desktop.width()
        desktopHeight = desktop.height()
        if posX + width > desktopWidth: posX = desktopWidth - width
        if posY + height > desktopWidth: posY = desktopHeight - height
        if posX < 0 : posX = 0
        
        Window_global.mainui.move( posX, posY )
        Window_global.mainui.resize( width, height )
        


def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    Window_global.mainui = Window( Window_global.mayawin )    
    
    Window_global.mainui.loadUIInfo()
    Window_global.mainui.show()
    