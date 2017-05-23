import pymel.core
import os
from sgModules import sgcommands

sceneName = cmds.file( q=1, sceneName=1 )
dirName = os.path.dirname( sceneName )
gpuPath = dirName + '/gpucaches'

sgcommands.makeFolder( gpuPath )

sels = cmds.ls( sl=1 )
sels.sort()

closeParents = []
for sel in sels:
    cloneParent = sgcommands.makeCloneObject( cmds.listRelatives( sel, p=1, f=1 )[0], cloneAttrName = '_clone' )
    abcPath = cmds.gpuCache( sel, startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=1, dataFormat='ogawa',
                             directory=gpuPath, fileName=sel, saveMultipleFiles=False )[0]
    gpuObjName = sel+'_gpu'
    gpuCacheNode = cmds.createNode( 'gpuCache' )
    gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
    gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
    gpuShapeName = cmds.listRelatives( gpuObjName, c=1,f=1 )[0]
    cmds.setAttr( gpuShapeName+'.cacheFileName', abcPath, type='string' )
    gpuCacheObj = cmds.parent( gpuCacheObj, cloneParent )
    cmds.xform( gpuCacheObj, os=1, matrix= sgcommands.matrixToList( sgcommands.OpenMaya.MMatrix() ) )