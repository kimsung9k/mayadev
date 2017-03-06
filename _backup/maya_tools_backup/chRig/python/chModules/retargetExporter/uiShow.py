import maya.cmds as cmds
import mainInfo
import addMenu
import addUserNameList
import addFileSearch
import addNamespace
import addLoadButton
import os

from functools import partial


class Cmd:
    
    def __init__(self):
        
        pass
            
    

class Show( Cmd ):
    
    def __init__(self):
        
        self._sideWidth = 7
        self._width = mainInfo.width - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__(self)
        
        
    def core(self):
        
        if cmds.window( mainInfo.winName, ex=1 ):
            cmds.deleteUI( mainInfo.winName, wnd=1 )
        cmds.window( mainInfo.winName, title = mainInfo.title, menuBar=True )
        
        addMenu.Add()
        
        cmds.columnLayout()
        
        cmds.rowColumnLayout( nc=2, cw=[ ( 1, mainInfo.userNameWidth ), ( 2, mainInfo.fileWidth ) ] )
        cmds.columnLayout()
        
        addUserNameList.Add()
        
        cmds.setParent( '..' )
        
        cmds.columnLayout()
        
        mainInfo.setSpaceH( 10 )
        
        addFileSearch.Add()
        
        mainInfo.setSpaceH( 10 )
        
        addNamespace.Add()
        
        cmds.setParent( '..' )
        
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 10 )
        
        addLoadButton.Add()
        
        cmds.window( mainInfo.winName, e=1, w=mainInfo.width, h=mainInfo.height )
        cmds.showWindow( mainInfo.winName )