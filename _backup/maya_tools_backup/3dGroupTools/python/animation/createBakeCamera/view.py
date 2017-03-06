import maya.cmds as cmds

from functools import partial
import os

import model
import uiModel
import cmdModel


class Model:
    targetExtensions = ['mb', 'ma', 'fbx', 'obj']
    
    


class SubWindow_BakedCamList:
    
    def __init__(self, winName ):
        
        self.parentWinName = winName
        self.winName = uiModel.winName+'_subWindow'
        self.title   = uiModel.title+' - Baked Camera List'

        self.scrollList = ''


    def editScrollList(self, strList ):
        
        cmds.textScrollList( self.scrollList, e=1, ra=1, append=strList)
        cmds.window( self.winName, e=1, h=len(strList)*13 + 5 )


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        scrollList = cmds.textScrollList()
        cmds.formLayout( form, e=1, 
                         af=[ (scrollList, 'top', 0 ), (scrollList, 'left', 0 ),
                              (scrollList, 'right', 0 ), (scrollList, 'bottom', 0 ) ] )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1 )
        cmds.showWindow( self.winName )
        top, Left = cmds.window( self.parentWinName, q=1, tlc=1 )
        width, height = cmds.window( self.parentWinName, q=1, wh=1 )
        
        cmds.window( self.winName, e=1, tlc=[top+height+37,Left], w=width, h=50 )

        self.scrollList = scrollList



class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        self.subWindow = SubWindow_BakedCamList( self.winName )
    
    
    def updatePopupMenu( self, textField, popupMenu ):
    
        cmds.popupMenu( popupMenu, e=1, dai=1 )
        cmds.setParent( popupMenu, menu=1 )
        path = cmds.textFieldGrp( textField, q=1, tx=1 )
        cmds.menuItem( l='Open File Browser', c=partial( cmdModel.openFileBrowser, path ) )
        cmds.menuItem( d=1 )
        
        def backToUpfolder( path, *args ):
            path = path.replace( '\\', '/' )
            path = '/'.join( path.split( '/' )[:-1] )
            cmds.textFieldGrp( textField, e=1, tx=path )
            self.updatePopupMenu( textField, popupMenu )
            
        if cmdModel.isFile(path) or cmdModel.isFolder(path):
            splitPath = path.replace( '\\', '/' ).split( '/' )
            if splitPath and splitPath[-1] != '':
                cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
        cmds.menuItem( d=1 )
        
        path = path.replace( '\\', '/' )
        if cmdModel.isFile(path):
            path = '/'.join( path.split( '/')[:-1] )
        
        def updateTextField( path, *args ):
            cmds.textFieldGrp( textField, e=1, tx=path )
            if textField == self.field_animPath:
                self.cmdChangeAnimPath()
            else: 
                self.updatePopupMenu( textField, popupMenu )
        
        for root, dirs, names in os.walk( path ):
            dirs.sort()
            for dir in dirs:
                cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
            names.sort()
            for name in names:
                extension = name.split( '.' )
                if len( extension ) == 1: continue
                extension = extension[1]
                if not extension.lower() in Model.targetExtensions:continue
                cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
            break


    def cmdChangeAnimPath(self, *args ):
        self.updatePopupMenu( self.field_animPath, self.pu_animPath )
        animPath = cmds.textFieldGrp( self.field_animPath, q=1, tx=1 )
        if cmdModel.isFile( animPath ):
            bakeCameraPath = cmdModel.getCameraPathFromAnimPath( animPath )
            cmds.textFieldGrp( self.field_bakePath, e=1, tx=bakeCameraPath )
            self.cmdChangeBakePath()


    def cmdChangeBakePath(self, *args ):
        self.updatePopupMenu( self.field_bakePath, self.pu_bakePath )
        

    def cmdBake(self, *args ):
        
        animationPath = cmds.textFieldGrp( self.field_animPath, q=1, tx=1 )
        bakeCameraPath = cmds.textFieldGrp( self.field_bakePath, q=1, tx=1 )
        cmdModel.bakeCamera( animationPath, bakeCameraPath )
        
        f = open( model.lastInfoPath, 'w' )
        f.write( animationPath.replace( '\\', '/' ) + '\n' + bakeCameraPath.replace( '\\', '/' ) )
        f.close()
        


    def cmdCheckCameraList(self, *args ):
        
        self.subWindow.create()
        
        animationPath = cmds.textFieldGrp( self.field_animPath, q=1, tx=1 )
        camList = cmdModel.getCameraList(animationPath)
        if camList:
            self.subWindow.editScrollList( camList )
        
        
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        firstWidth = (columnWidth-2)*0.3
        secondWidth = (columnWidth-2) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        field_animPath   = cmds.textFieldGrp( l='Animation Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                              cc=self.cmdChangeAnimPath )
        pu_animPath      = cmds.popupMenu()
        field_bakePath   = cmds.textFieldGrp( l='Bake Camera Path : ', cw=[(1,firstWidth),(2,secondWidth)],
                                              cc=self.cmdChangeBakePath )
        pu_bakePath    = cmds.popupMenu()
        cmds.text( l='', h=5 )
        cmds.button( l='Bake', c= self.cmdBake )
        cmds.button( l='Check Baked Camera List', c= self.cmdCheckCameraList )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.field_animPath = field_animPath
        self.pu_animPath = pu_animPath
        self.field_bakePath = field_bakePath
        self.pu_bakePath = pu_bakePath
        
        try:
            f = open( model.lastInfoPath, 'r' )
            data = f.read()
            f.close()
            animPath, bakeCamPath = data.split( '\n' )
            cmds.textFieldGrp( field_animPath, e=1, tx=animPath )
            self.cmdChangeAnimPath()
            cmds.textFieldGrp( field_bakePath, e=1, tx=bakeCamPath )
            self.cmdChangeBakePath()
        except: pass