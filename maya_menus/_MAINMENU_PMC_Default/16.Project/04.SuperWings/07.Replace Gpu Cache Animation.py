import maya.cmds as cmds
import os
sceneName = cmds.file( q=1, sceneName=1 )
folderPath = os.path.dirname( sceneName )

fileName = sceneName.split( '/' )[-1]
cutName = '_'.join( fileName.split( '_' )[:2] ) + '_animatedTrees'

targetPath = folderPath + '/' + cutName
if os.path.exists( targetPath ):
    gpuCaches = cmds.ls( type='gpuCache' )
    for cache in gpuCaches:
        filePath = cmds.getAttr( cache + '.cacheFileName' )
        if filePath.find( 'EP237_animatedTrees' ) == -1: continue
        replacedPath = filePath.replace( 'EP237_animatedTrees', cutName )
        if not os.path.exists( replacedPath ): continue
        cmds.setAttr( cache + '.cacheFileName', replacedPath, type='string' )