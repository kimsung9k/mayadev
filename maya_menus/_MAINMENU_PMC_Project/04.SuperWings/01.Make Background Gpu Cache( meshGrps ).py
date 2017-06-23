import pymel.core
import os
from sgModules import sgcommands

sceneName = cmds.file( q=1, sceneName=1 )
dirName = os.path.dirname( sceneName )
gpuPath = dirName + '/gpucaches2'

sgcommands.makeFolder( gpuPath )

sels = cmds.ls( sl=1 )
sels.sort()

closeParents = []
defaultMatrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
for sel in sels:
    selPos = cmds.getAttr( sel + '.wm' )
    cmds.xform( sel, os=1, matrix=defaultMatrix )
    selFileName = sel.replace( '|', '_' )
    cloneParent = sgcommands.makeCloneObject( cmds.listRelatives( sel, p=1, f=1 )[0], cloneAttrName = '_clone' )
    abcPath = cmds.gpuCache( sel, startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=1, dataFormat='ogawa',
                             directory=gpuPath, fileName=selFileName, saveMultipleFiles=False )[0]
    gpuObjName = sel.split( '|' )[-1]+'_gpu'
    gpuCacheNode = cmds.createNode( 'gpuCache' )
    gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
    gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
    gpuShapeName = cmds.listRelatives( gpuObjName, c=1,f=1 )[0]
    cmds.setAttr( gpuShapeName+'.cacheFileName', abcPath, type='string' )
    gpuCacheObj = cmds.parent( gpuCacheObj, cloneParent )
    cmds.xform( gpuCacheObj, os=1, matrix= selPos )
    cmds.setAttr( sel + '.v', 0 )