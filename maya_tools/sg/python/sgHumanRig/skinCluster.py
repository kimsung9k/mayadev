import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import dag
from sgModules import sgbase
import copy
import attribute
import convert




def getSkinCluster( mesh ):
    
    hists = cmds.listHistory( mesh, pdo=1 )

    for hist in hists:
        if cmds.nodeType( hist ) == "skinCluster": return hist
    
    return None




class Weight_perVtx:
    
    def __init__(self, plugWeightListElement ):
        
        self.plugWeights = plugWeightListElement.child(0)
        self.jointIndices = []
        self.weightValues = []
        self.getWeight()


    def getWeight(self):
        
        for i in range( self.plugWeights.numElements() ):
            self.jointIndices.append( self.plugWeights[i].logicalIndex() )
            self.weightValues.append( self.plugWeights[i].asFloat() )


    def setWeight(self, jointIndices, weights ):
        
        attribute.removeMultiInstances( self.plugWeights.name() )
        for i in range( len( jointIndices ) ):
            cmds.setAttr( self.plugWeights.name() + '[%d]' % jointIndices[i], weights[i] )


def printMatrix( mtx ):
    
    return convert.matrixToList( mtx )



class Node:

    def __init__(self, skinCluster ):
        
        self.fnNode = OpenMaya.MFnDependencyNode( sgbase.getMObject( skinCluster ) )
        
        self.plugMatrix  = self.fnNode.findPlug( 'matrix' )
        self.plugBindPre = self.fnNode.findPlug( 'bindPreMatrix' )
        
        self.jointMatrices = self.getJointMatrices()
        self.jointOriginalMatrices = self.getJointOriginalMatrices()
        self.jointBindPres = self.getJointBindPres()
        self.weightInfos   = self.getWeightInfos()
    

    
    def getJointMatrices(self):
        
        numElements = self.plugMatrix.numElements()
        matList = []
        for i in range( numElements ):
            matObject = self.plugMatrix[i].asMObject()
            matData = OpenMaya.MFnMatrixData( matObject )
            matList.append( copy.copy(matData.matrix()) )
        return matList
        

    
    def getJointOriginalMatrices(self):
        
        numElements = self.plugBindPre.numElements()
        matList = []
        for i in range( numElements ):
            matObject = self.plugBindPre[i].asMObject()
            matData = OpenMaya.MFnMatrixData( matObject )
            matList.append( matData.matrix().inverse() )
        return matList
    


    def getJointBindPres(self):
        
        numElements = self.plugBindPre.numElements()
        matList = []
        for i in range( numElements ):
            matObject = self.plugBindPre[i].asMObject()
            matData = OpenMaya.MFnMatrixData( matObject )
            matList.append( matData.matrix() )
        return matList
    


    def getWeightInfos(self):
        
        plugWeightList = self.fnNode.findPlug( "weightList" )
        
        weightInfos = []
        for i in range( plugWeightList.numElements() ):
            weightInfos.append( Weight_perVtx( plugWeightList[i] ) )
        return weightInfos



def rebind( target ):
    
    pass




def replaceSkinClusterJoint( jntBefore, jntAfter, skinedMesh ):
    
    skinClusterNode = dag.getNodeFromHistory( skinedMesh, 'skinCluster', pdo=1 )
    if not skinClusterNode: return None
    
    connectedAttrs = cmds.listConnections( jntBefore + '.wm', type='skinCluster', p=1 )
    
    for connectedAttr in connectedAttrs:
        node = connectedAttr.split( '.' )[0]
        if not node in skinClusterNode: continue
        cmds.connectAttr( jntAfter + '.wm', connectedAttr, f=1 )
    
    
    


def inverseSkinClusterConnect( origMesh, targetShape, skinedMesh ):
    
    origShape = dag.getShape( origMesh )
    skinShape = dag.getShape( skinedMesh )
    targetShape = dag.getShape( targetShape )
    
    skinNode = dag.getNodeFromHistory( skinShape, 'skinCluster', pdo=1 )[0]
    
    fixObj = cmds.duplicate( origShape )[0]
    fixShape = dag.getShape( fixObj )
    
    node = cmds.deformer( fixShape, type='sgInverseSkinCluster' )[0]
    
    cmds.connectAttr( skinShape + '.wm', node + '.geomMatrix' )
    cmds.connectAttr( skinNode + '.message', node + '.targetSkinCluster' )
    cmds.connectAttr( targetShape + '.outMesh', node + '.inMesh' )




def autoCopyWeight( first, second ):
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
    
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )




def weightToR( targetObj ):
    
    hists = cmds.listHistory( targetObj )
    
    skinNode = ''
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            break
            
    if not skinNode: return None

    cmds.copySkinWeights( ss=skinNode, ds=skinNode, mirrorMode = 'YZ',
                          surfaceAssociation = 'closestComponent', influenceAssociation = ['oneToOne','closestJoint'] )



def weightToL( targetObj ):
    
    hists = cmds.listHistory( targetObj )
    
    skinNode = ''
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            break
            
    if not skinNode: return None
    
    cmds.copySkinWeights( ss=skinNode, ds=skinNode, mirrorMode = 'YZ', mirrorInverse=True,
                          surfaceAssociation = 'closestComponent', influenceAssociation = ['oneToOne','closestJoint'] )




def toolSmoothBrush():
    
    import maya.mel as mel
    
    _cmdStr =  """global string $tf_skinSmoothPatin_selection[];
    
    global proc tf_smoothBrush( string $context )     
    {       
     artUserPaintCtx -e -ic "tf_init_smoothBrush"
     -svc "tf_set_smoothBrushValue"
     -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }
    
    global proc tf_init_smoothBrush( string $name )
    {
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        
        sgSmoothWeightCommand $obj;
    }
    
    global proc tf_set_smoothBrushValue( int $slot, int $index, float $val )             
    {         
        sgSmoothWeightCommand -i $index -w $val;
    }
    
    ScriptPaintTool;     
    artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;"""
    
    if not cmds.pluginInfo( 'sgSmoothWeightCommand', q=1, loaded=1 ):
        cmds.loadPlugin( 'sgSmoothWeightCommand' )
    mel.eval( _cmdStr )

        



def toolHardBrush():
    
    import maya.mel as mel
    
    _cmdStr =  """global string $tf_skinHardPatin_selection[];
    
    global proc tf_hardBrush( string $context )     
    {       
     artUserPaintCtx -e -ic "tf_init_hardBrush"
     -svc "tf_set_hardBrushValue"
     -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }
    
    global proc tf_init_hardBrush( string $name )
    {
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        
        sgSmoothWeightCommand $obj;
    }
    
    global proc tf_set_hardBrushValue( int $slot, int $index, float $val )             
    {
        sgSmoothWeightCommand -h 1 -i $index -w $val;
    }
    
    ScriptPaintTool;     
    artUserPaintCtx -e -tsc "tf_hardBrush" `currentCtx`;"""
    
    if not cmds.pluginInfo( 'sgSmoothWeightCommand', q=1, loaded=1 ):
        cmds.loadPlugin( 'sgSmoothWeightCommand' )
    mel.eval( _cmdStr )




def lockAllJoints():

    for jnt in cmds.ls( type='joint' ):
        if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
        cmds.setAttr( jnt+'.lockInfluenceWeights', 1 )




def unlockAllJoints():

    for jnt in cmds.ls( type='joint' ):
        if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
        cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )
        



def bindSkin( jntGrp, meshGrp ):
    
    childrenJnts = cmds.listRelatives( jntGrp, c=1, ad=1, f=1, type='joint' )
    if not childrenJnts: childrenJnts = []
    if cmds.nodeType( jntGrp ) == 'joint':
        childrenJnts.append( jntGrp )
    
    meshs = cmds.listRelatives( meshGrp, c=1, ad=1, f=1, type='mesh' )
    
    targetMeshs = []
    for mesh in meshs:
        if cmds.getAttr( mesh + '.io' ): continue
        meshTr = cmds.listRelatives( mesh, p=1, f=1 )[0]
        if not meshTr in targetMeshs:
            targetMeshs.append( meshTr )
    
    cmds.select( childrenJnts, targetMeshs )
    cmds.SmoothBindSkin()




    
def combineSkinCluster( skinedObjs ):
    
    numVertices = None
    
    skinedObjs = dag.getMeshTransforms( skinedObjs )
    
    for skinedObj in skinedObjs:
        objShape = dag.getShape( skinedObj )
        fnMesh = OpenMaya.MFnMesh( dag.getDagPath( objShape ) )
        if not numVertices:
            numVertices = fnMesh.numVertices()
        else:
            if numVertices != fnMesh.numVertices():
                cmds.error( "Selected meshs not same objects" )
    
    skinJoints = []
    weightList = [ [] for i in range( numVertices ) ]
    for skinedObj in skinedObjs:
        
        skinCluster = dag.getNodeFromHistory( skinedObj, 'skinCluster' )
        if not skinCluster: continue
        
        skinCluster = skinCluster[0]
        
        fnNode = OpenMaya.MFnDependencyNode( sgbase.getMObject( skinCluster ) )
        
        plugMatrix = fnNode.findPlug( 'matrix' )
        
        plugMatrixMaxLogicalIndex = 0
        for i in range( plugMatrix.numElements() ):
            logicalIndex = plugMatrix[i].logicalIndex()
            if logicalIndex > plugMatrixMaxLogicalIndex:
                plugMatrixMaxLogicalIndex = logicalIndex 
        
        connections = OpenMaya.MPlugArray()
        skinedJointIndices = []
        origSkinedJointIndicesMap = [ -1 for i in range( plugMatrixMaxLogicalIndex+1 ) ]
        for i in range( plugMatrix.numElements() ):
            
            plugMatrix[i].connectedTo( connections, True, False )
            if not connections.length():
                continue
            
            skinJointName = OpenMaya.MFnDagNode( connections[0].node() ).fullPathName()
            
            if not skinJointName in skinJoints:
                skinJoints.append( skinJointName )
            
            jntIndex = skinJoints.index( skinJointName )
            origSkinedJointIndicesMap[ plugMatrix[i].logicalIndex() ] = jntIndex
            skinedJointIndices.append( jntIndex )
    
        plugWeightList = fnNode.findPlug( 'weightList' )
        
        for i in range( plugWeightList.numElements() ):
            
            plugWeights = plugWeightList[i].child( 0 )
            for j in range( plugWeights.numElements() ):
                
                logicalIndex = plugWeights[j].logicalIndex()
                weightValue = plugWeights[j].asFloat()
                jntIndex = origSkinedJointIndicesMap[ logicalIndex ]
                
                weightList[i].append( [jntIndex, weightValue] )
    
    newMesh = cmds.createNode( 'mesh' )
    srcShape = dag.getShape( skinedObjs[0] )
    newMeshObj = dag.getParent( newMesh )
    cmds.connectAttr( srcShape+'.outMesh', newMesh+'.inMesh' )
    cmds.refresh()
    cmds.disconnectAttr( srcShape+'.outMesh', newMesh+'.inMesh' )
    node = cmds.deformer( newMeshObj, type='skinCluster' )[0]
    
    for i in range( len( skinJoints ) ):
        cmds.connectAttr( skinJoints[i]+'.wm', node+'.matrix[%d]' % i )
        bindPreMatrix = cmds.getAttr( skinJoints[i]+'.wim' )
        cmds.setAttr( node+'.bindPreMatrix[%d]' % i, bindPreMatrix, type='matrix' )
    
    for i in range( len( weightList ) ):
        for logicalIndex, value in weightList[i]:
            cmds.setAttr( node+'.weightList[%d].weights[%d]' %( i, logicalIndex ), value )
    
    cmds.skinPercent( node, normalize=True )
            
    
    
    
    
    
def setBindPreDefault( meshs ):
    
    for sel in meshs:
        hists = cmds.listHistory( sel )
        
        skinNode = None
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = hist
                break
        
        fnSkinNode = OpenMaya.MFnDependencyNode( sgbase.getMObject( skinNode ) )
        
        plugMatrix = fnSkinNode.findPlug( 'matrix' )
        plugBindPre = fnSkinNode.findPlug( 'bindPreMatrix' )
        
        for i in range( plugMatrix.numElements() ):
            loIndex = plugMatrix[i].logicalIndex()
            oMtx = plugMatrix[i].asMObject()
            mtxData = OpenMaya.MFnMatrixData( oMtx )
            mtx = mtxData.matrix()
            invData = OpenMaya.MFnMatrixData()
            oInv = invData.create( mtx.inverse() )
            plugBindPre.elementByLogicalIndex( loIndex ).setMObject( oInv )
