import maya.cmds as cmds
import maya.OpenMaya as om
import functions as fnc
import baseCommand as bc
import maya.mel as mel


def cleanShape( shapeObj ):
    
    shapes = cmds.listRelatives( shapeObj, s=1 )

    if not shapes: return None

    for shape in shapes:
        ioValue = cmds.getAttr( shape+'.io' )
        if ioValue:
            cmds.delete( shape )



def blendMeshAssign( target, deformObj, driverIndices=[], driverWeights=[], targetIndex=None ):
    
    node = fnc.getNodeFromHist( deformObj, 'blendAndFixedShape' )
    
    if not node:
        node = bc.blendAndFix_toSkin( deformObj )
    
    if not node:
        node = cmds.deformer( deformObj, type='blendAndFixedShape' )[0]
        
    meshObjs = cmds.listConnections( node, s=1, d=0, type='mesh' )
    
    if meshObjs:
        if target in meshObjs:
            targetShape = cmds.listRelatives( target, s=1 )[0]
            attrName = targetShape+'.outMesh'
            fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
            blendMeshInfoPlugs = fnNode.findPlug( 'blendMeshInfos' )
            numElements = blendMeshInfoPlugs.numElements()
            for i in range( numElements ):
                inputMeshPlug = blendMeshInfoPlugs[i].child( 0 )
                cons = om.MPlugArray()
                inputMeshPlug.connectedTo( cons, True, False )
                
                if cons.length():
                    if cons[0].name() == attrName:
                        targetIndex = i
                        cmds.removeMultiInstance( "%s[%d]" %( blendMeshInfoPlugs.name(), targetIndex ) )
                        print blendMeshInfoPlugs.name(), i, 'is deleted'
                        break
        
    if not targetIndex == None:
        assignNum = targetIndex
    else:
        fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
        blendMeshInfoPlug = fnNode.findPlug( 'blendMeshInfos' )
        assignNum = blendMeshInfoPlug.numElements()
    
    targetShape = cmds.listRelatives( target, s=1 )[0]
    cmds.connectAttr( targetShape+'.outMesh', node+'.blendMeshInfos[%d].inputMesh' % assignNum )
    
    for i in range( len( driverIndices ) ):
        index = driverIndices[i]
        weight = driverWeights[i]
        
        cmds.setAttr( node+'.blendMeshInfos[%d].targetWeights[%d]' %( assignNum, index ), weight )