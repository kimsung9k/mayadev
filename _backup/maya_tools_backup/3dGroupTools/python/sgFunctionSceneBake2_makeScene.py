import sys
import cPickle
import maya.standalone

maya.standalone.initialize( name='python' )

import maya.cmds as cmds

import maya.mel as mel
mayaDocPath = mel.eval( 'getenv MAYA_APP_DIR' )

sysPathInfoPath = mayaDocPath + '/LocusCommPackagePrefs/sgStandalone/sysPath.txt'
standaloneInfoPath = mayaDocPath + '/LocusCommPackagePrefs/sgStandalone/sgFunctionSceneBake2_makeScene.txt'

f = open( sysPathInfoPath, 'r' )
sysPaths = cPickle.load( f )
f.close()


for path in sysPaths:
    if not path in sys.path:
        sys.path.append( path )

import sgFunctionFileAndPath
import sgRigAttribute
import sgModelDg


f = open( standaloneInfoPath, 'r' )
scenePaths, bakeInfoPaths = cPickle.load( f )
f.close()

for i in range( len( scenePaths ) ):
    
    scenePath = scenePaths[i]
    bakeInfoPath = bakeInfoPaths[i]
    sgFunctionFileAndPath.makeFile( scenePath, False )
    
    cmds.file( f=1, new=1 )
    
    f = open( bakeInfoPath, 'r' )
    bakeTargetList = cPickle.load( f )
    f.close()
    
    bakeInfoPath = bakeInfoPath.replace( '\\', '/' )
    sceneInfoPath = '/'.join( bakeInfoPath.split( '/' )[:-1]) + '/sceneInfo.sceneInfo'
    
    f = open( sceneInfoPath, 'r' )
    timeUnit, minTime, maxTime = cPickle.load( f )
    f.close()
    
    cmds.currentUnit( time = timeUnit )
    
    for k in range( len( bakeTargetList ) ):
        #print "bakeTrargetList : ", bakeTargetList[k]
        tr = bakeTargetList[k][0]
        
        for j in range( len( bakeTargetList[k][3] ) ):
            attr = bakeTargetList[k][3][j][0]
            info = bakeTargetList[k][3][j][1]
            animCurve = info.createAnimCurve()
            #animCurve = cmds.rename( animCurve, 'sceneBake_animCurve_for_%s' %( tr.split( '|' )[-1]+'_'+attr ) )
            sgRigAttribute.addAttr( animCurve, ln='bakeTargetAttrName', dt='string' )
            cmds.setAttr( animCurve+'.bakeTargetAttrName', tr+'.'+attr, type='string' )
            
    cmds.file( rename=scenePath )
    cmds.file( f=1, save=1,  options="v=0;", type="mayaAscii" )