import math
import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDg, sgModelDag


def getSkinClusterFromMesh( mesh ):
    
    return sgModelDag.getNodeFromHistory( mesh, 'skinCluster' )



def getInfluenceAndWeightList( mesh, vertices = [] ):

    skinClusters = sgModelDag.getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusters: return None
    
    skinCluster = skinClusters[0]
    
    fnSkinCluster = sgModelDg.getDependNode( skinCluster )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    if not vertices: vertices = [ i for i in range( plugWeightList.numElements() ) ]
    influenceAndWeightList = [ [] for i in range( len( vertices ) ) ]
    phygicalMap = [ 0 for i in range( plugWeightList.numElements() ) ]
    
    for i in range( len( vertices ) ):
        logicalIndex = vertices[i]
        plugWeights = plugWeightList[ logicalIndex ].child( 0 )
        influenceNums = []
        values = []
        for j in range( plugWeights.numElements() ):
            influenceNum = plugWeights[j].logicalIndex()
            value = plugWeights[j].asFloat()
            influenceNums.append( influenceNum )
            values.append( value )
        
        influenceAndWeightList[i] = [ influenceNums, values ]
        phygicalMap[ logicalIndex ] = i
        
    return influenceAndWeightList, phygicalMap



def getPlugMatrix( mesh ):
    
    skinCluster = getSkinClusterFromMesh( mesh )
    if not skinCluster: return None
    skinCluster = skinCluster[0]
    fnSkinCluster = sgModelDg.getDependNode( skinCluster )
    
    return fnSkinCluster.findPlug( 'matrix' )



def getPlugBindPre( mesh ):
    
    skinCluster = getSkinClusterFromMesh( mesh )
    if not skinCluster: return None
    skinCluster = skinCluster[0]
    fnSkinCluster = sgModelDg.getDependNode( skinCluster )
    
    return fnSkinCluster.findPlug( 'bindPreMatrix' )

        
        