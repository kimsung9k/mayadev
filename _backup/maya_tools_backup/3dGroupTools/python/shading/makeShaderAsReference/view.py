import maya.cmds as cmds
import maya.mel as mel

import uiModel
import cmdModel
import functions
from functools import partial

import UIs.saveCheck


def updatePopupCmdDefault( textFieldGrp, popupMenu, *args ):
    
    functions.updatePopupMenu( textFieldGrp, popupMenu, updatePopupCmdDefault )


class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
    
    
    def cmdChangeOpenPath(self, *args):
        
        functions.updatePopupMenu( self.fd_openPath, self.pu_openPath, updatePopupCmdDefault )
        openPath = cmds.textFieldGrp( self.fd_openPath, q=1, tx=1 )
        cmdModel.PathToFile.setOpenPathFromFile( openPath )


    def cmdChangeShaderPath(self, *args ):
        
        functions.updatePopupMenu( self.fd_shaderPath, self.pu_shaderPath, updatePopupCmdDefault )
        shaderPath = cmds.textFieldGrp( self.fd_shaderPath, q=1, tx=1 )
        cmdModel.PathToFile.setShaderPathFromFile( shaderPath )


    def cmdOpenToLocalPath(self, *args ):
        
        openPath = cmds.textFieldGrp( self.fd_openPath, q=1, tx=1 )
        cmd = partial( cmdModel.copyFromServerAndOpen, openPath )
        UIs.saveCheck.Window( self.winName, cmd )
        
        
    def cmdBackup(self, *args ):
        
        currentPath = cmds.file( q=1, sceneName=1 )
        openPath = cmds.textFieldGrp( self.fd_openPath, q=1, tx=1 )
        cmdModel.backup( currentPath, openPath )
        
        
    def cmdBackupShaderAsReference(self, *args ):
        
        shaderPath = cmds.textFieldGrp( self.fd_shaderPath, q=1, tx=1 )
        exportOnly = cmds.checkBox( self.cb_ExportOlny, q=1, v=1 )
        cmdModel.backupShaderAdReference( shaderPath, exportOnly )


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        firstWidth  = ( columnWidth -2 )* 0.23
        secondWidth = ( columnWidth -2 ) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( l='', h=5 )
        fd_openPath = cmds.textFieldGrp( l='Open Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                        cc=self.cmdChangeOpenPath )
        pu_openPath = cmds.popupMenu()
        cmds.text( l='', h=5 )
        cmds.button( l='Open to Local Path', c=self.cmdOpenToLocalPath )
        cmds.button( l='Back up', c=self.cmdBackup )
        cmds.separator()
        cmds.text( l='', h=5 )
        fd_shaderPath = cmds.textFieldGrp( l='Shader Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                        cc=self.cmdChangeShaderPath )
        pu_shaderPath = cmds.popupMenu()
        cmds.text( l='', h=3 )
        cmds.rowColumnLayout( nc=2, cw=[(1,20),(2,columnWidth-2-50)])
        cmds.text( l='' )
        cb_ExportOlny = cmds.checkBox( l='  Export Only' )
        cmds.setParent('..')
        cmds.text( l='', h=5 )
        cmds.button( l='Backup Shader as Reference', c= self.cmdBackupShaderAsReference, h=25 )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.fd_openPath = fd_openPath
        self.pu_openPath = pu_openPath
        self.fd_shaderPath = fd_shaderPath
        self.pu_shaderPath = pu_shaderPath
        self.cb_ExportOlny = cb_ExportOlny
        
        path = cmdModel.PathToFile.getOpenPathFromFile()
        cmds.textFieldGrp( fd_openPath, e=1, tx=path )
        updatePopupCmdDefault( self.fd_openPath, self.pu_openPath, updatePopupCmdDefault )
        
        path = cmdModel.PathToFile.getShaderPathFromFile()
        cmds.textFieldGrp( fd_shaderPath, e=1, tx=path )
        updatePopupCmdDefault( self.fd_shaderPath, self.pu_shaderPath, updatePopupCmdDefault )