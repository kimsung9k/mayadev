import maya.mel as mel
import maya.cmds as cmds
import os
from functools import partial

import model


def isFile( path ):
    
    return os.path.isfile( path )



def isFolder( path ):
    
    return os.path.isdir( path )



def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        
        
def makeFile( pathName ):
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makePath( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()



def openFileBrowser( path='', *args ):
    
    if not isFile( path ) and not isFolder( path ):
        cmds.warning( 'Path is not Exists' )
    
    path = path.replace( '\\', '/' )
    if isFile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )



def updatePopupMenu( textField, popupMenu, updateTextFieldCmd ):
    
    cmds.popupMenu( popupMenu, e=1, dai=1 )
    cmds.setParent( popupMenu, menu=1 )
    path = cmds.textFieldGrp( textField, q=1, tx=1 )
    cmds.menuItem( l='Open File Browser', c=partial( openFileBrowser, path ) )
    cmds.menuItem( d=1 )
    
    def backToUpfolder( path, *args ):
        path = path.replace( '\\', '/' )
        path = '/'.join( path.split( '/' )[:-1] )
        cmds.textFieldGrp( textField, e=1, tx=path )
        updatePopupMenu( textField, popupMenu, updateTextFieldCmd )
        
    if isFile(path) or isFolder(path):
        splitPath = path.replace( '\\', '/' ).split( '/' )
        if splitPath and splitPath[-1] != '':
            cmds.menuItem( l='Back', c=partial( backToUpfolder, path ) )
    cmds.menuItem( d=1 )
    
    path = path.replace( '\\', '/' )
    if isFile(path):
        path = '/'.join( path.split( '/')[:-1] )
    
    def updateTextField( path, *args ):
        cmds.textFieldGrp( textField, e=1, tx=path )
        updateTextFieldCmd( textField, popupMenu )
    
    for root, dirs, names in os.walk( path ):
        dirs.sort()
        for dir in dirs:
            cmds.menuItem( l= dir, c= partial( updateTextField, root+'/'+dir ) )
        names.sort()
        for name in names:
            extension = name.split( '.' )
            if len( extension ) == 1: continue
            extension = extension[1]
            if not extension.lower() in model.targetExtensions:continue
            cmds.menuItem( l= name, c= partial( updateTextField, root+'/'+name ) )
        break