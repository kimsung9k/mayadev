from maya import cmds
from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

for sel in sels:
    gpuPath = sel.definition.get()
    folderName = '/'.join( gpuPath.split( '/' )[:-1] )
    assetName = folderName.split( '/' )[-1]
    filePath = folderName + '/' + assetName + '_.mb'
    cmds.file( filePath, r=1, type="mayaBinary", ignoreVersion=1, gl=1,
               mergeNamespacesOnClash=False, namespace=sel.name()+'_', options="v=0;" )
    pos = pymel.core.xform( sel, q=1, ws=1, matrix=1 )
    refObj = pymel.core.ls( sel.name() + '_:SET' )[0]
    pymel.core.xform( refObj, ws=1, matrix= pos )