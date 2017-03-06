from maya import cmds
import os, json


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



def writeCamData( camInfomationPath, camTransform, minFrame, maxFrame ):
    
    camShape = cmds.listRelatives( camTransform, s=1, f=1 )[0]

    camInfomation = {"name": camTransform,
                    "timeUnit":cmds.currentUnit( q=1, time=1 ),
                    "minFrame":minFrame,
                    "maxFrame":maxFrame,
                    "interval":1,
                    "matrix":[] }
    camAttrs = cmds.listAttr( camShape, k=1 )
    for attr in camAttrs:
        try:
            cmds.getAttr( camShape + '.' + attr )
            camInfomation.update( { attr : [] } )
        except:pass
    
    intervalMult = int( 1.0/camInfomation['interval'] )
    for i in range( minFrame * intervalMult, maxFrame * intervalMult + 1 ):
        cmds.currentTime( int( float(i) / intervalMult ) )
        camInfomation[ 'matrix' ].append( cmds.getAttr( camTransform + '.wm' ) )
        for attr in camAttrs:
            if not camInfomation.has_key( attr ): continue
            camInfomation[ attr ].append( cmds.getAttr( camShape + '.' + attr ) )
    
    f = open( camInfomationPath, 'w' )
    json.dump( camInfomation, f, indent=2 )
    f.close()




def makeCamScene( bakeCamPath, camInfomationPath ):

    f = open( camInfomationPath, 'r' )
    camInfomation = json.load( f )
    f.close()
    
    camTransform, camShape = cmds.camera()
    camAttrs = cmds.listAttr( camShape, k=1 )

    camName = camInfomation['name']
    timeUnit = camInfomation['timeUnit']
    minFrame = camInfomation['minFrame']
    maxFrame = camInfomation['maxFrame']
    interval = camInfomation['interval']
    
    cmds.currentUnit( time=timeUnit )
    cmds.playbackOptions( min=minFrame, max=maxFrame )
    
    camTransform = cmds.rename( camTransform, camName )
    camShape     = cmds.listRelatives( camTransform, s=1, f=1 )[0]
    
    intervalMult = int( 1.0/interval )
    for i in range( minFrame * intervalMult, maxFrame * intervalMult + 1 ):
        cmds.currentTime( float(i) / intervalMult )
        
        matrixValue = camInfomation[ 'matrix' ][i-minFrame]
        cmds.xform( camTransform, ws=1, matrix= matrixValue )
        for attr in camAttrs:
            if camInfomation.has_key( attr ):
                try:cmds.setAttr( camShape + '.' + attr, camInfomation[attr][i-minFrame] )
                except:pass
        cmds.setKeyframe( camTransform, camShape )
    
    cmds.file( rename=bakeCamPath )
    cmds.file( f=1, options="v=0", typ="mayaAscii", save=1 )
    
    os.remove( camInfomationPath )
    
    print "success : %s" % bakeCamPath



def exportCamera( camGrp, minFrame, maxFrame, exportPath ):

    minFrame = int( minFrame )
    maxFrame = int( maxFrame )

    camExportLaunchString = """
import maya.standalone
import maya.cmds as cmds
import sys
maya.standalone.initialize( name='python' )

sys.path.append( '@modulePath@' )

import _MODULENAME_
_MODULENAME_.makeCamScene( "@cameraPath@", "@infomationPath@" )
"""

    def getCurrentModelPanels():
        pannels = cmds.getPanel( vis=1 )
        modelPanels = []
        for pannel in pannels:
            if cmds.modelPanel( pannel, ex=1 ):
                modelPanels.append( pannel )
        return modelPanels
    
    allTrs = cmds.listRelatives( camGrp, c=1, ad=1, f=1 )
    allTrs.append( camGrp )
    
    camShape = ''
    for tr in allTrs:
        cams = cmds.listRelatives( tr, s=1, type='camera' )
        if not cams: continue
        camShape = cams[0]
    
    if not camShape: return None
    camTransform = cmds.listRelatives( camShape, p=1, f=1 )[0]
    cmds.select( camTransform )
    
    pannels = getCurrentModelPanels()
    
    for pannel in pannels:
        cmds.isolateSelect( pannel, state=1 )
    
    sceneName = cmds.file( q=1, sceneName=1 )
    camInfomationPath = os.path.dirname( sceneName ) + '/%s_caminfomation.txt' % sceneName.split( '/' )[-1].split( '.' )[0]
    makeFile( camInfomationPath )

    writeCamData( camInfomationPath, camTransform, minFrame, maxFrame )
    
    for pannel in pannels:
        cmds.isolateSelect( pannel, state=0 )
    
    import maya.mel as mel
    modulePath = os.path.dirname( __file__ )
    mayapyPath = mel.eval( 'getenv MAYA_LOCATION' ) + '/bin/mayapy.exe'
    launchPath = ( modulePath + '/camExportLaunch.py' ).replace( '\\', '/' )
    
    exportDir = os.path.dirname( exportPath )
    makeFolder( exportDir )
    
    camExportLaunchString = camExportLaunchString.replace( '@modulePath@', modulePath ).replace( '@cameraPath@', exportPath ).replace( '@infomationPath@', camInfomationPath ).replace( '_MODULENAME_', __name__.split( '.' )[-1] )
    
    f = open( launchPath, 'w' )
    f.write( camExportLaunchString )
    f.close()
    
    mel.eval( 'system( "start %s %s" )' %( mayapyPath, launchPath ) )




        