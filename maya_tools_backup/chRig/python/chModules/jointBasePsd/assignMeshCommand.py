import maya.cmds as cmds
import maya.OpenMaya as om
import functions as fnc
import math


def getBlendAndFixedShapeNode( meshObject ):
    
    hists = cmds.listHistory( meshObject, pdo=1 )
        
    if not hists: return None
    
    skinClusterEx = False
    
    for hist in hists:
        if skinClusterEx:
            if cmds.nodeType( hist ) == 'blendAndFixedShape':
                return hist
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinClusterEx = True
            continue
    
    return None



def addMirrorTarget( meshObj, index ):
    
    cmds.addMirrorBlendMeshInfos( meshObj, i=index, mi=0, rei=0 )

    blendAndFixed = getBlendAndFixedShapeNode( meshObj )
    if not blendAndFixed: return None
    
    fnBlendAndFixed = om.MFnDependencyNode( fnc.getMObject( blendAndFixed ) )
    plugBlendMeshInfo = fnBlendAndFixed.findPlug( "blendMeshInfos" )
    plugBlendMeshElementTarget = plugBlendMeshInfo[ plugBlendMeshInfo.numElements()-1 ]
    plugWeightsTarget = plugBlendMeshElementTarget.child( 2 )
    plugNameTarget = plugBlendMeshElementTarget.child( 3 )
    plugAnimCurveTarget = plugBlendMeshElementTarget.child( 5 )
    plugAnimOutputTarget = plugBlendMeshElementTarget.child( 6 )

    plugMeshInfoElement = plugBlendMeshInfo[index]
    plugTargetWeights = plugMeshInfoElement.child( 2 )
    plugOrigName = plugMeshInfoElement.child( 3 )
    plugAnimCurve = plugMeshInfoElement.child( 5 )
    
    nameOrig = plugOrigName.asString()
    if nameOrig.find( '_L_' ) != -1:
        replacedName = nameOrig.replace( '_L_', '_R_' )
    elif nameOrig.find( '_R_' ) != -1:
        replacedName = nameOrig.replace( '_R_', '_L_' )
    else:
        replacedName = nameOrig+'_inv'
        
    plugNameTarget.setString( replacedName )
    
    cons = cmds.listConnections( plugAnimCurve.name() )
    if cons:
        duAnim = cmds.duplicate( cons[0] )[0]
        duAnim = cmds.rename( duAnim, replacedName+'_anim' )
        cmds.connectAttr( duAnim+'.message', plugAnimCurveTarget.name() )
        cmds.connectAttr( duAnim+'.output', plugAnimOutputTarget.name() )

    numElements = plugTargetWeights.numElements()

    logicalIndices = []
    weightValues = []
    for i in range( numElements ):
        logicalIndices.append( plugTargetWeights[i].logicalIndex() )
        weightValues.append( plugTargetWeights[i].asFloat() )
    
    nodeName = fnBlendAndFixed.name()
    driverWeightsPlug = fnBlendAndFixed.findPlug( 'driverWeights' )
    fnc.clearNoneConnectedElements( driverWeightsPlug )
    connectIndex = driverWeightsPlug[ driverWeightsPlug.numElements()-1 ].logicalIndex() + 1
    
    driverInfos = []
    for i in range( numElements ):
        driverInfo = [None, 0,0,0 ]
        attrName = nodeName+'.driverWeights[%d]' % logicalIndices[i]
        cons = cmds.listConnections( attrName, s=1, d=0, p=1, c=1 )
        if not cons:
            continue
        
        edited = False
        if cons[1].find( '_L_' ) != -1:
            invTarget = cons[1].replace( '_L_', '_R_' )
            edited = True
        elif cons[1].find( '_R_' ) != -1:
            invTarget = cons[1].replace( '_R_', '_L_' )
            edited = True
        else:
            invTarget = cons[1]
        
        invNode, attrName = invTarget.split( '.' )
        driverInfo[0] = invNode
        
        driverInfoWeight = 0
        if edited:
            driverInfoWeight = weightValues[i]
        else:
            driverInfoWeight = -weightValues[i]
        
        if attrName == 'outDriver0':
            driverInfo[1] = driverInfoWeight
        elif attrName == 'outDriver1':
            driverInfo[2] = driverInfoWeight
        elif attrName == 'outDriver2':
            driverInfo[3] = driverInfoWeight
        
        if not cmds.objExists( invNode ):
            return None
        
        cons = cmds.listConnections( invTarget, d=1, s=0, p=1, c=1, type='blendAndFixedShape' )

        if not cons:
            cmds.connectAttr( invTarget, nodeName+'.driverWeights[%d]' % connectIndex )
            cmds.setAttr( "%s[%d]" %( plugWeightsTarget.name(), connectIndex ), driverInfoWeight  )
            connectIndex += 1
        else:
            print cons
            driverWeightIndex = int( cons[1].split( '[' )[1].replace( ']', '' ) )
            cmds.setAttr( "%s[%d]" %( plugWeightsTarget.name(), driverWeightIndex ), driverInfoWeight )
        driverInfos.append( driverInfo )
            
    return replacedName,  driverInfos, plugBlendMeshElementTarget.logicalIndex()
        


class Main:
    
    def __init__(self, editMesh, targetMesh, driverAndAttr, minValue=0.1 ):
        
        self._minValue = minValue
        self._driverAndAttr = driverAndAttr
        self._editMesh = editMesh
        self._targetMesh = targetMesh
        
        self.connectMovedDriverToFixedNode()
        self.connectMesh()
        self.deleteMeshs()


    def connectMovedDriverToFixedNode(self):
        
        targetMesh = self._targetMesh
        node = getBlendAndFixedShapeNode( targetMesh )
        
        attrs = []
        
        for driver, attr in self._driverAndAttr:
            value0 = cmds.getAttr( driver+'.'+attr )
            attrs.append( driver+'.'+attr )
        
        self._connectIndices = []
        self._connectWeights = []
        
        for attr in attrs:
            blendAndFixedShapeCons = cmds.listConnections( attr, type='blendAndFixedShape' )
            
            if not blendAndFixedShapeCons:
                targetIndex = fnc.getLastIndex( node+'.driverWeights' )+1
                cmds.connectAttr( attr, node+'.driverWeights[%d]' % targetIndex )
                self._connectIndices.append( targetIndex )
                self._connectWeights.append( value0 )
                continue
            
            if not node in blendAndFixedShapeCons:
                continue
            
            cons = cmds.listConnections( attr, p=1, c=1 )
            targetAttr = cons[1]
            
            connectedIndex = int( targetAttr.split('[')[1].replace(']','' ) )
            connectedValue = cmds.getAttr( cons[1] )
            self._connectIndices.append( connectedIndex )
            self._connectWeights.append( connectedValue )
            
    
    def connectMesh( self ):
        
        targetMesh = self._targetMesh
        targetShape = cmds.listRelatives( targetMesh, s=1 )[0]
        print "%s exists : " % self._editMesh, cmds.objExists( self._editMesh )
        editMeshShape = cmds.listRelatives( self._editMesh, s=1 )[0]
        skinNode = self.getSkinCluster( targetShape )
        if not skinNode: return None
        
        origShape = fnc.getOrigShape( targetShape )
        
        inverseMesh = cmds.createNode( 'mesh' )
        cmds.connectAttr( origShape+'.outMesh', inverseMesh+'.inMesh' )
        
        inverseSkinNode = cmds.deformer( inverseMesh, type='inverseSkinCluster' )[0]
        
        cmds.connectAttr( targetMesh+'.wm', inverseSkinNode+'.geomMatrix' )
        cmds.connectAttr( editMeshShape+'.outMesh', inverseSkinNode+'.inMesh' )
        cmds.connectAttr( skinNode+'.message', inverseSkinNode+'.targetSkinCluster' )
        
        cmds.disconnectAttr( self._editMesh+'.message', targetMesh+'.editMesh' )
        
        node = getBlendAndFixedShapeNode( targetMesh )
        
        connectIndex = fnc.getLastIndex( node+'.blendMeshInfos' )+1
        
        inverseMeshObj = cmds.listRelatives( inverseMesh, p=1 )[0]
        keepEditMeshName = self._editMesh
        self._editMesh = cmds.rename( self._editMesh, self._editMesh+'_tempEditMesh' )
        inverseMeshObj = cmds.rename( inverseMeshObj, keepEditMeshName )
        inverseMesh = cmds.listRelatives( inverseMeshObj, s=1 )[0]
        cmds.assignBlendMeshInfo( inverseMesh, node )
        
        for i in range( len( self._connectIndices ) ):
            index = self._connectIndices[i]
            value = self._connectWeights[i]
            cmds.setAttr( node+'.blendMeshInfos[%d].targetWeights[%d]' %( connectIndex, index ), value )
        
        cmds.setAttr( self._editMesh+'.v', 0 )
        cmds.setAttr( targetMesh+'.v', 1 )
        
        self.addMatrixInfo( node, skinNode, connectIndex )
        
        self._inverseMesh = inverseMeshObj
        self._assignIndex = connectIndex
        self._node  = node
        
        
    def deleteMeshs(self):
        
        cmds.refresh()
        cmds.delete( self._inverseMesh )
        cmds.delete( self._editMesh  )
        
        
    def addMatrixInfo(self, node,skinNode, index ):
        
        fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
        infoPlug = fnNode.findPlug( "blendMeshInfos" )
        plugElement = infoPlug.elementByLogicalIndex( index );
        keepMatrixPlug = plugElement.child( 4 )
        
        fnSkinNode = om.MFnDependencyNode( fnc.getMObject( skinNode ) )
        matrixPlug = fnSkinNode.findPlug( "matrix" )
        
        for i in range( matrixPlug.numElements() ):
            logicalIndex = matrixPlug[i].logicalIndex()
            matrixObj = matrixPlug[i].asMObject()
            keepMatrixElement = keepMatrixPlug.elementByLogicalIndex( logicalIndex )
            keepMatrixElement.setMObject( matrixObj )
        
        
    def getSkinCluster(self, mesh ):
        
        hists = cmds.listHistory( mesh )
        
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                return hist
            
        return None