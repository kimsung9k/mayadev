import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel


def setGlobalEditMeshShader( target ):
    
    blinns = cmds.ls( type='blinn' )
        
    editMeshShader=None
    for blinn in blinns:
        if cmds.attributeQuery( 'isEditMeshShader', node=blinn, ex=1 ):
            editMeshShader = blinn
            
    if not editMeshShader:
        blinn = cmds.shadingNode( 'blinn', asShader=1 )
        editMeshShader = cmds.rename( blinn, 'EditMeshShader' )
        SG = cmds.sets( renderable=True, noSurfaceShader=True, empty=1, n='EditMeshSG' )
        cmds.connectAttr( editMeshShader+'.outColor', SG+'.surfaceShader' )
        cmds.setAttr( editMeshShader+'.color', .2,1,.6, type='double3' )
        cmds.setAttr( editMeshShader+'.specularColor', .2,.2,.2, type='double3' )
    else:
        SG = cmds.listConnections( editMeshShader+'.outColor' )[0]
    
    cmds.sets( target, e=1, forceElement=SG )



def getMObject( nodeName ):
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj



class DeltaInfo:
    
    def __init__( self, attrName, logicalIndex ):
        self._attrName = attrName
        self._logical = logicalIndex
        
        

def getPsdJointBaseNode( target ):
    
    hists = cmds.listHistory( target )
    
    node = None
    skinCluster = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'psdJointBase':
            node = hist
            continue
        if cmds.nodeType( hist ) == 'skinCluster':
            skinCluster = hist
            break
    
    if not skinCluster: return None
    
    if not node:
        node = cmds.deformer( target, type='psdJointBase' )[0]
        cmds.connectAttr( skinCluster+'.message', node+'.skinCluster' )
        
    return node



def getShapeList( meshObj ):
    
    node = getPsdJointBaseNode( meshObj )
    
    fnNode = om.MFnDependencyNode( getMObject( node ) )
    
    plugDeltaInfo = fnNode.findPlug( 'deltaInfo' )
    
    infoList = []
    for i in range( plugDeltaInfo.numElements() ):
        logicalIndex = plugDeltaInfo[i].logicalIndex()
        
        infoList.append( DeltaInfo( plugDeltaInfo[i].name(), logicalIndex ) )
    
    return infoList



def createEditMesh( target ):
    
    duTarget = cmds.duplicate( target )[0]
    cmds.addAttr( duTarget, ln='isEditMesh', at='bool' )
    
    setGlobalEditMeshShader( duTarget )
    
    if not cmds.attributeQuery( 'editMesh', node=target, ex=1 ):
        cmds.addAttr( target, ln='editMesh', at='message' )
    cmds.connectAttr( duTarget+'.message', target+'.editMesh', f=1 )
    cmds.setAttr( target+'.v', 0 )



def assignMesh( target ):
    
    cmds.setAttr( target+'.v', 1 )
    cons = cmds.listConnections( target+'.editMesh' )
    if not cons: cmds.error( "Edit mesh connection is not exist" )
    editMesh = cons[0]
    
    editMeshShapes = cmds.listRelatives( editMesh, s=1 )
    for shape in editMeshShapes:
        if cmds.getAttr( shape+'.v' ) == 1 and cmds.getAttr( shape+'.io' ) == 0:
            editMeshShape = shape
            
    node = getPsdJointBaseNode( target )
    fnNode = om.MFnDependencyNode( getMObject( node ) )
    plugDeltaInfo = fnNode.findPlug( 'deltaInfo' )
    
    lastIndex = plugDeltaInfo.numElements()-1
    if lastIndex == -1:
        targetLogical = 0
    else:
        lastLogical = plugDeltaInfo[ lastIndex ].logicalIndex()
        targetLogical = lastLogical + 1
    
    mel.eval( "psdJointBase_addShape %s %s" % ( editMesh, target ) )
    #cmds.connectAttr( editMeshShape+'.outMesh', node+'.deltaInfo[%d].inputMesh' % targetLogical )
    
    cmds.refresh()
    cmds.delete( editMesh )
    


def indexAssignMesh( target, index ):
    
    cmds.setAttr( target+'.v', 1 )
    cons = cmds.listConnections( target+'.editMesh' )
    if not cons:
        createEditMesh( target )
        return None
    editMesh = cons[0]
    
    editMeshShapes = cmds.listRelatives( editMesh, s=1 )
    for shape in editMeshShapes:
        if cmds.getAttr( shape+'.v' ) == 1 and cmds.getAttr( shape+'.io' ) == 0:
            editMeshShape = shape
            
    node = getPsdJointBaseNode( target )
    fnNode = om.MFnDependencyNode( getMObject( node ) )
    plugDeltaInfo = fnNode.findPlug( 'deltaInfo' )
    
    lastIndex = plugDeltaInfo.numElements()-1
    if lastIndex == -1:
        targetLogical = 0
    else:
        lastLogical = plugDeltaInfo[ lastIndex ].logicalIndex()
        targetLogical = lastLogical + 1
    
    cmds.psdJointBase_addShape( editMesh, target, i=index )
    #cmds.connectAttr( editMeshShape+'.outMesh', node+'.deltaInfo[%d].inputMesh' % targetLogical )
    
    cmds.refresh()
    cmds.delete( editMesh )