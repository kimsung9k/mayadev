import pymel.core
import os
from sgMaya import sgCmds

sceneName = cmds.file( q=1, sceneName=1 )
dirName = os.path.dirname( sceneName )
gpuPath = dirName + '/gpucaches'

sgCmds.makeFolder( gpuPath )

sels = cmds.ls( sl=1 )

closeParents = []
for sel in sels:
    selParents = cmds.listRelatives( sel, p=1, f=1 )
    selPos = cmds.getAttr( sel+ '.m' )
    cmds.xform( sel, os=1, matrix= sgCmds.matrixToList( sgCmds.OpenMaya.MMatrix() ) )
    abcPath = cmds.gpuCache( sel, startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=0, dataFormat='ogawa',
                             directory=gpuPath, fileName=sel.replace( '|', '_' ), saveMultipleFiles=False )[0]
    cmds.xform( sel, os=1, matrix= selPos )
    if cmds.objExists( sel+'_gpu' ): continue
    gpuObjName = sel.split( '|' )[-1]+'_gpu'
    gpuCacheNode = cmds.createNode( 'gpuCache' )
    gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
    gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
    gpuShapeName = cmds.listRelatives( gpuCacheObj, c=1,f=1 )[0]
    cmds.setAttr( gpuShapeName+'.cacheFileName', abcPath, type='string' )
    if selParents:
        gpuCacheObj = cmds.parent( gpuCacheObj, selParents[0] )
    cmds.xform( gpuCacheObj, os=1, matrix= selPos )
    cmds.setAttr( sel + '.v', 1 )
    
    cmds.connectAttr( gpuCacheObj + '.t', sel + '.t' )
    cmds.connectAttr( gpuCacheObj + '.r', sel + '.r' )
    cmds.connectAttr( gpuCacheObj + '.s', sel + '.s' )