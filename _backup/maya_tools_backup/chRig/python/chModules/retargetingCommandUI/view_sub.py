from model import *

import maya.cmds as cmds


class RenameUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self, *args ):
        
        top, left = cmds.window( WindowInfo._window, q=1, topLeftCorner=1 )
        
        top  += 70
        left +=19
        
        itemIndex = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, sii=1 )
        if not itemIndex: return None
        selItem = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )[0].split('.')[0]
        
        top += itemIndex[0]*13
        
        if cmds.window( FolderSubRenameUiInfo._winName, ex=1 ):
            cmds.deleteUI( FolderSubRenameUiInfo._winName )
        cmds.window( FolderSubRenameUiInfo._winName, titleBar=0 )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=3, cw=[(1,120),(2,52),(3,25)] )
        textField = cmds.textField( tx=selItem )
        cmds.button( l='Rename', c=FolderSubRenameUiInfo.cmdRename )
        cmds.button( l='X' , c=self.cmdDeleteWindow, bgc=[0.9,0.35,0.35] )
        
        cmds.windowPref( FolderSubRenameUiInfo._winName, e=1,
                         widthHeight = [ FolderSubRenameUiInfo._width, FolderSubRenameUiInfo._height ],
                         topLeftCorner = [ top, left ] )
        cmds.showWindow( FolderSubRenameUiInfo._winName )
        
        FolderSubRenameUiInfo._renameTextField = textField


    def cmdDeleteWindow(self, *args ):
        
        cmds.deleteUI( FolderSubRenameUiInfo._winName, wnd=1 )
        
        
class DeleteUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self, *args ):
        
        top, left = cmds.window( WindowInfo._window, q=1, topLeftCorner=1 )
        
        top  +=70
        left +=19
        
        itemIndex = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, sii=1 )
        if not itemIndex: return None
        
        top += itemIndex[0]*13
        
        if cmds.window( FolderSubDeleteUiInfo._winName, ex=1 ):
            cmds.deleteUI( FolderSubDeleteUiInfo._winName )
        cmds.window( FolderSubDeleteUiInfo._winName, titleBar=0 )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,200)] )
        cmds.text( l='Are You Sure?', al='center', h=22 )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=2, cw=[(1,100),(2,100)])
        cmds.button( l='Delete', c=FolderSubDeleteUiInfo.cmdDelete, h=22 )
        cmds.button( l='Cancel', c=self.cmdDeleteWindow, h=22 )
        cmds.setParent( '..' )
        
        cmds.windowPref( FolderSubDeleteUiInfo._winName, e=1,
                         widthHeight = [ FolderSubDeleteUiInfo._width, FolderSubDeleteUiInfo._height ],
                         topLeftCorner = [ top, left ] )
        cmds.showWindow( FolderSubDeleteUiInfo._winName )

    def cmdDeleteWindow( self, *args ):
        
        cmds.deleteUI( FolderSubDeleteUiInfo._winName, wnd=1 )