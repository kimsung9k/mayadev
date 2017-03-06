import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDg


def getMultiAttrIndices( node, attr ):
    
    fnNode = om.MFnDependencyNode( sgModelDg.getMObject( node ) )
    
    plugAttr = fnNode.findPlug( attr )
    
    logicalIndices = []
    for i in range( plugAttr.numElements() ):
        logicalIndices.append( plugAttr[i].logicalIndex() )
    
    return logicalIndices