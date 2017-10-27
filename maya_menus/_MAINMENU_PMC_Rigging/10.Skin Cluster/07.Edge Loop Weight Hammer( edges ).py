from sgModules import sgcommands
from maya import OpenMaya
import maya.cmds as cmds

selEdges = cmds.ls( sl=1, fl=1 )

for edge in selEdges:
    vertices = cmds.ls( cmds.polyListComponentConversion( edge, tv=1 ), fl=1 )
    vtxIndex = int( vertices[0].split( '[' )[-1].replace( ']', '' ) )
    
    meshName = edge.split( '.' )[0]
    meshShape = cmds.listRelatives( meshName, s=1, f=1 )[0]
    skinNodes = sgcommands.getNodeFromHistory( meshName, 'skinCluster' )
    if not skinNodes: continue
    
    fnSkinNode = OpenMaya.MFnDependencyNode( sgcommands.getMObject( skinNodes[0] ) )
    plugWeightList = fnSkinNode.findPlug('weightList')
    weightsPlug = plugWeightList[vtxIndex].child(0)
    
    indicesAndValues = []
    for i in range( weightsPlug.numElements() ):
        influenceIndex = weightsPlug[i].logicalIndex()
        value = weightsPlug[i].asFloat()
        indicesAndValues.append( [influenceIndex,value] )
    
    cmds.select( edge )
    edgeLoop = cmds.SelectEdgeLoopSp()
    edges = cmds.ls( sl=1, fl=1 )
    vertices = cmds.ls( cmds.polyListComponentConversion( edges, tv=1 ), fl=1 )
    for vtx in vertices:
        vtxIndex = int( vtx.split( '[' )[-1].replace( ']', '' ) )
        eachWeightsPlug = plugWeightList[ vtxIndex ].child(0)
        for i in range( eachWeightsPlug.numElements() ):
            cmds.removeMultiInstance( eachWeightsPlug[0].name() )
        for influenceIndex, value in indicesAndValues:
            cmds.setAttr( skinNodes[0] + '.weightList[%d].weights[%d]' % (vtxIndex, influenceIndex), value )

cmds.select( selEdges )