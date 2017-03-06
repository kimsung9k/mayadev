import maya.mel as mel
import maya.cmds as cmds
import os
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
        path = model.defaultFileBrowserPath
    
    path = path.replace( '\\', '/' )
    if isFile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )
    
    
    
def getCameraPathFromAnimPath( animPath, *args ):
    
    animPath = animPath.replace( '\\', '/' )
    splits = animPath.split( '/' )
    cutName   = splits[-3]
    shotName  = splits[-4]
    
    mainFolder = '/'.join( splits[:-2] ) + '/layout/anicam'
    bakeCameraPath = mainFolder+'/'+shotName+cutName+'_camera_bake.mb'
    
    return bakeCameraPath



def getInfoLastInfoFromFile():
    
    lastInfoFile = model.lastInfoPath
    makeFile( lastInfoFile )
    
    f = open( lastInfoFile, 'r' )
    data = f.read()
    f.close()
    
    return data



def bakeCamera( animationPath, bakeCameraPath ):
    
    data = animationPath+'\n'+bakeCameraPath
    
    makeFile( model.infoPath )
    
    f = open( model.infoPath, 'w' )
    f.write( data )
    f.close()
    
    mel.eval( 'system( "start %s %s" )' %( model.mayapyPath, model.launchPath ) )
    
    
    
def getCameraList( animationPath ):
    
    cameraListLocalPath = '/'.join( animationPath.replace( '\\', '/' ).split('/')[:-1] )+'/camList.txt'
    makeFile( cameraListLocalPath )
    
    f = open( cameraListLocalPath, 'r' )
    camListInfo = f.read()
    f.close()
    
    if not camListInfo: return None
    camListInfo = camListInfo.replace( '\\', '/' ).split( '\n' )

    camNameList = []
    for camName in camListInfo:
        camName = camName.strip()
        camNameList.append( camName )
    
    return camNameList