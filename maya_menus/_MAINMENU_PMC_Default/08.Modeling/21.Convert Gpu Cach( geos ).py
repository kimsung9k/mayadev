import pymel.core
import os
from sgModules import sgcommands
reload( sgcommands )

sceneName = cmds.file( q=1, sceneName=1 )
dirName = os.path.dirname( sceneName )
gpuPath = dirName + '/gpucaches'

sgcommands.makeFolder( gpuPath )

sels = cmds.ls( sl=1 )

closeParents = []
for sel in sels:
    selParent = cmds.listRelatives( sel, p=1, f=1 )[0]
    selPos = cmds.getAttr( sel+ '.m' )
    cmds.xform( sel, os=1, matrix= sgcommands.matrixToList( sgcommands.OpenMaya.MMatrix() ) )
    abcPath = cmds.gpuCache( sel, startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=1, dataFormat='ogawa',
                             directory=gpuPath, fileName=sel.replace( '|', '_' ), saveMultipleFiles=False )[0]
    cmds.xform( sel, os=1, matrix= selPos )
    if cmds.objExists( sel+'_gpu' ): continue
    gpuObjName = sel.split( '|' )[-1]+'_gpu'
    gpuCacheNode = cmds.createNode( 'gpuCache' )
    gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
    gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
    gpuShapeName = cmds.listRelatives( gpuCacheObj, c=1,f=1 )[0]
    cmds.setAttr( gpuShapeName+'.cacheFileName', abcPath, type='string' )
    gpuCacheObj = cmds.parent( gpuCacheObj, selParent )[0]
    cmds.xform( gpuCacheObj, os=1, matrix= selPos )
    cmds.setAttr( sel + '.v', 0 )
    
    cmds.connectAttr( gpuCacheObj + '.t', sel + '.t' )
    cmds.connectAttr( gpuCacheObj + '.r', sel + '.r' )
    cmds.connectAttr( gpuCacheObj + '.s', sel + '.s' )