import pymel.core
from maya import cmds, OpenMaya
import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

src = sels[0]
dst = sels[1]

srcSkin = sgCmds.getNodeFromHistory( src, 'skinCluster' )[0]
dstSkin = sgCmds.getNodeFromHistory( dst, 'skinCluster' )[0]

fnSrcSkin = OpenMaya.MFnDependencyNode( sgCmds.getMObject( srcSkin.name() ) )
fnDstSkin = OpenMaya.MFnDependencyNode( sgCmds.getMObject( dstSkin.name() ) )

srcWeightList = fnSrcSkin.findPlug( 'weightList' )
dstWeightList = fnDstSkin.findPlug( 'weightList' )

for i in range( dstWeightList.numElements() ):
    weightsPlugDst = dstWeightList[i].child(0)
    for j in range( weightsPlugDst.numElements() ):
        cmds.removeMultiInstance( weightsPlugDst[0].name() )
    
    weightsPlugSrc = srcWeightList[i].child(0)
    for j in range( weightsPlugSrc.numElements() ):
        logicalIndex = weightsPlugSrc[j].logicalIndex()
        cmds.setAttr( weightsPlugDst.name() + '[%d]' % logicalIndex, weightsPlugSrc[j].asFloat() )