import maya.cmds as cmds
import maya.OpenMaya as om
import copy


def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj



def getDist( first, second ):
    
    return ( ( second[0] - first[0] )**2 + ( second[1] - first[1] )**2 + ( second[2] - first[2] )**2 ) **0.5



def appendInfluence( skinCluster, jnt, vtxIndices ):
    
    fnSkinCluster = om.MFnDependencyNode( getMObject( skinCluster ) )
    
    plugMatrix = fnSkinCluster.findPlug( 'matrix' )
    if plugMatrix.numElements():
        appendIndex = plugMatrix[ plugMatrix.numElements()-1 ].logicalIndex()
    else:
        appendIndex = 0
    
    cmds.connectAttr( jnt+'.wm', skinCluster+'.matrix[%d]' % appendIndex )
    cmds.setAttr( skinCluster+'.bindPreMatrix[%d]' % appendIndex, cmds.getAttr( jnt+'.wim' ), type='matrix' )
    for index in vtxIndices:
        cmds.setAttr( skinCluster+'.weightList[%d].weights[%d]' %( index, appendIndex ), 1.0 )
    
    if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ):
        cmds.addAttr( jnt, ln='lockInfluenceWeights', at='bool' )
    
    cmds.connectAttr( jnt+'.lockInfluenceWeights', skinCluster+'.lockWeights[%d]' % appendIndex )
    
    
def setJointInfluence( skinCluster, jnt, vtxIndices ):
    
    cons = cmds.listConnections( jnt+'.wm', type='skinCluster', c=1, p=1, d=1, s=0 )
    if not cons: return None
    for con in cons:
        if con.find( skinCluster ) != -1:
            skinClusterAttr = con
    fnSkinCluster = om.MFnDependencyNode( getMObject( skinCluster ) )
    
    jntIndex = int( skinClusterAttr.split( '[' )[-1].replace( ']', '' ) )
    
    weightListPlug = fnSkinCluster.findPlug( 'weightList' )
    
    for vtxIndex in vtxIndices:
        weightListPlugElement = weightListPlug.elementByLogicalIndex( vtxIndex )
        weightPlug = weightListPlugElement.child( 0 )
        for i in range( weightPlug.numElements() ):
            cmds.removeMultiInstance( weightPlug[0].name() )
        cmds.setAttr( skinCluster+'.weightList[%d].weights[%d]' %( vtxIndex, jntIndex ), 1.0 )
        
        

def setJointsInfluence( mesh, jnts, vtxIndices ):
    
    hists = cmds.listHistory( mesh )
    
    skinCluster = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinCluster = hist
            break
    if not skinCluster: return None
    
    cons = []
    for jnt in jnts:
        cons += cmds.listConnections( jnt+'.wm', type='skinCluster', c=1, p=1, d=1, s=0 )

    print jnts
    print 'skinCluster : ', skinCluster
    skinClusterAttrs = []
    for con in cons:
        if con.find( skinCluster ) != -1:
            if not con in skinClusterAttrs:
                skinClusterAttrs.append( con )
    fnSkinCluster = om.MFnDependencyNode( getMObject( skinCluster ) )
    
    jntIndices = []
    for skinClusterAttr in skinClusterAttrs:
        jntIndex = int( skinClusterAttr.split( '[' )[-1].replace( ']', '' ) )
        jntIndices.append( jntIndex )

    jntPoses = []
    for jnt in jnts:
        childJnt = cmds.listRelatives( jnt, c=1, f=1 )
        if not childJnt:
            pos = cmds.xform( jnt, q=1, ws=1, piv=1 )[:3]
            jntPoses.append( pos )
        else:
            childPos = cmds.xform( childJnt[0], q=1, ws=1, piv=1 )[:3]
            pos = cmds.xform( jnt, q=1, ws=1, piv=1 )[:3]
            sumPos = ( (childPos[0] + pos[0]) *0.5, (childPos[1] + pos[1]) *0.5, (childPos[2] + pos[2]) *0.5 )
            jntPoses.append( sumPos )
    
    print len( jntIndices ), len( jntPoses )
    weightListPlug = fnSkinCluster.findPlug( 'weightList' )
    
    for vtxIndex in vtxIndices:
        vtxPos = cmds.xform( mesh+'.vtx[%d]' % vtxIndex, q=1, ws=1, t=1 )[:3]
        
        minDist = 100000000
        secondMinDist = 100000000
        minDistIndex = 0
        secondMinDistIndex = 1
        for i in range( len(jntPoses) ):
            dist = getDist( vtxPos, jntPoses[i] )
            if minDist > dist:
                secondMinDist = copy.copy( minDist )
                minDist = dist
                secondMinDistIndex = copy.copy( minDistIndex )
                minDistIndex = i 
            elif secondMinDist > dist:
                secondMinDist = dist
                secondMinDistIndex = i
            
        weightListPlugElement = weightListPlug.elementByLogicalIndex( vtxIndex )
        weightPlug = weightListPlugElement.child( 0 )
        
        for i in range( weightPlug.numElements() ):
            cmds.removeMultiInstance( weightPlug[0].name() )
        
        allDist = minDist + secondMinDist
        secondMinWeightValue = (minDist/allDist)**2
        minWeightValue = 1-secondMinWeightValue
        
        cmds.setAttr( skinCluster+'.weightList[%d].weights[%d]' %( vtxIndex, jntIndices[minDistIndex] ), minWeightValue )
        cmds.setAttr( skinCluster+'.weightList[%d].weights[%d]' %( vtxIndex, jntIndices[secondMinDistIndex] ), secondMinWeightValue )

        


class CopyVtxAndPast:
    
    def __init__(self, meshName ):
        
        hists = cmds.listHistory( meshName )
    
        skinCluster = ''
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinCluster = hist
        
        if not skinCluster: return None
        
        fnSkinCluster = om.MFnDependencyNode( getMObject( skinCluster ) ) 
        self.weightListPlug = fnSkinCluster.findPlug( 'weightList' )


    def getWeightAndPast(self, index, indices ):
    
        weightListPlugElement = self.weightListPlug.elementByLogicalIndex( index )
        plugWeights = weightListPlugElement.child( 0 )
        
        indicesAndValues = []
        for i in range( plugWeights.numElements() ):
            index = plugWeights[i].logicalIndex()
            value = plugWeights[i].asFloat()
            indicesAndValues.append( [index,value] )
        
        for vtxIndex in indices:
            weightListPlugElement = self.weightListPlug.elementByLogicalIndex( vtxIndex )
            plugWeights = weightListPlugElement.child( 0 )
            for i in range( plugWeights.numElements() ):
                cmds.removeMultiInstance( plugWeights[0].name() )
            for index, value in indicesAndValues:
                cmds.setAttr( plugWeights.name() + '[%d]' % index, value )


        
def copyVtxAndPast( meshName, index, indices ):
    
    hists = cmds.listHistory( meshName )
    
    skinCluster = ''
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinCluster = hist
    
    if not skinCluster: return None
    
    fnSkinCluster = om.MFnDependencyNode( getMObject( skinCluster ) )
    weightListPlug = fnSkinCluster.findPlug( 'weightList' )
    
    weightListPlugElement = weightListPlug.elementByLogicalIndex( index )
    plugWeights = weightListPlugElement.child( 0 )
    
    indicesAndValues = []
    for i in range( plugWeights.numElements() ):
        index = plugWeights[i].logicalIndex()
        value = plugWeights[i].asFloat()
        indicesAndValues.append( [index,value] )
    
    for vtxIndex in indices:
        weightListPlugElement = weightListPlug.elementByLogicalIndex( vtxIndex )
        plugWeights = weightListPlugElement.child( 0 )
        for i in range( plugWeights.numElements() ):
            cmds.removeMultiInstance( plugWeights[0].name() )
        for index, value in indicesAndValues:
            cmds.setAttr( plugWeights.name() + '[%d]' % index, value )