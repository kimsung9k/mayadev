import maya.standalone
import maya.cmds as cmds
import maya.mel as mel
import sys, os
from functools import partial
import sgFunctionStandaloneLaunch
import sgModelFileAndPath
import sgFunctionFileAndPath
import cPickle
    


def sgFunctionSceneBake2_makeScene( scenePaths, bakeInfoPaths, standaloneInfoPath ):
    
    launchPath = ''
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        dirList = os.listdir( path )
        if 'sgFunctionStandaloneLaunch' in dirList:
            launchPath = path+'/sgFunctionStandaloneLaunch/sgFunctionSceneBake2_makeScene.py'

    sysPathInfoPath = sgModelFileAndPath.getLocusCommPackagePrefsPath() + '/sgStandalone/sysPath.txt'
    
    sgFunctionFileAndPath.makeFile( sysPathInfoPath, False )
    sgFunctionFileAndPath.makeFile( standaloneInfoPath, False )
    
    f = open( sysPathInfoPath, 'w' )
    cPickle.dump( sys.path, f )
    f.close()
    
    f = open( standaloneInfoPath, 'w' )
    cPickle.dump( [ scenePaths, bakeInfoPaths ], f )
    f.close()
    
    mel.eval( 'system( "start %s %s" )' %( sgModelFileAndPath.getMayaPyPath(), launchPath ) )



def moveFile( srcPath, targetPath ):
    
    launchPath = ''
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        dirList = os.listdir( path )
        if 'sgFunctionStandaloneLaunch' in dirList:
            launchPath = path+'/sgFunctionStandaloneLaunch/sgMoveFile.py'
    
    moveFileInfo = sgModelFileAndPath.getLocusCommPackagePrefsPath() + '/sgStandalone/moveFile.txt'
    sysPathInfoPath = sgModelFileAndPath.getLocusCommPackagePrefsPath() + '/sgStandalone/sysPath.txt'
    
    sgFunctionFileAndPath.makeFile( sysPathInfoPath, False )
    sgFunctionFileAndPath.makeFile( moveFileInfo, False )
    
    f = open( sysPathInfoPath, 'w' )
    cPickle.dump( sys.path, f )
    f.close()
    
    f = open( moveFileInfo, 'w' )
    cPickle.dump( [srcPath, targetPath], f )
    f.close()
    
    mel.eval( 'system( "start %s %s" )' %( sgModelFileAndPath.getMayaPyPath(), launchPath ) )