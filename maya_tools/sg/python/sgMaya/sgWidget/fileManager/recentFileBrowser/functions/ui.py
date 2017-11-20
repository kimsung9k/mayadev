import maya.cmds as cmds
from functools import *
import path as pathFunctions
import os


def updatePathPopupMenu( textField, popupMenu, addCommand=None ):

    targetExtensions = ['mb', 'ma', 'fbx', 'obj']
    
    cmds.popupMenu( popupMenu, e=1, dai=1 )
    cmds.setParent( popupMenu, menu=1 )
    path = cmds.textFieldGrp( textField, q=1, tx=1 )
    cmds.menuItem( l='Open File Browser', c=partial( pathFunctions.openFileBrowser, path ) )
    cmds.menuItem( d=1 )
    
    def backToUpfolder( path, *args ):
        path = path.replace( '\\', '/' )
        path = '/'.join( path.split( '/' )[:-1] )
        cmds.textFieldGrp( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu, addCommand )
        
    if pathFunctions.isFile(path) or pathFunctions.isFolder(path):
        splitPath = path.replace( '\\', '/' ).split( '/' )
        if splitPath and splitPath[-1] != '':
            cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
    cmds.menuItem( d=1 )
    
    path = path.replace( '\\', '/' )
    if pathFunctions.isFile(path):
        path = '/'.join( path.split( '/')[:-1] )
    
    def updateTextField( path, *args ):
        cmds.textFieldGrp( textField, e=1, tx=path )
        updatePathPopupMenu( textField, popupMenu )
        if( addCommand != None ): addCommand()
    
    for root, dirs, names in os.walk( path ):
        dirs.sort()
        for dir in dirs:
            cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
        names.sort()
        for name in names:
            extension = name.split( '.' )
            if len( extension ) == 1: continue
            extension = extension[1]
            if not extension.lower() in targetExtensions:continue
            cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
        break