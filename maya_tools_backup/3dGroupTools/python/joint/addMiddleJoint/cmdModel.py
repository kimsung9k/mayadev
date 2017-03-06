import maya.cmds as cmds


def createMiddleJoint( targetJoint, offset ):
    
    jointParent = cmds.listRelatives( targetJoint, p=1 )
    
    if not jointParent: return None
    
    jointParent = jointParent[0]
    
    transformNode = cmds.createNode( 'transform', n=targetJoint+'_mdJnt_base' )
    cmds.parent( transformNode, jointParent )
    cmds.xform( transformNode, matrix=cmds.getAttr( targetJoint+'.m' ) )
    cmds.select( transformNode )
    targetJointRadius = cmds.getAttr( targetJoint+'.radius' )
    middleJoint = cmds.joint( rad=targetJointRadius*1.5, n=targetJoint+'_mdJnt' )
    
    cmds.connectAttr( targetJoint+'.t', transformNode+'.t' )
    blendMatrix = cmds.createNode( 'blendTwoMatrixDecompose' )
    
    cmds.connectAttr( targetJoint+'.m', blendMatrix+'.inMatrix1' )
    cmds.connectAttr( blendMatrix+'.or', transformNode+'.r' )
    cmds.setAttr( middleJoint+'.t', *offset )




def uiCmd_createMiddleJoint( offset, *args ):
    
    selections = cmds.ls( sl=1 )
    
    for selection in selections:
        createMiddleJoint( selection, offset )