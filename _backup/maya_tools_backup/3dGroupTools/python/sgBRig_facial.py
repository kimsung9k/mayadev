import maya.cmds as cmds
import maya.OpenMaya as om


def setEyeRotation( topJoint, closeValue = 40 ):
    
    import sgBFunction_attribute
    
    childJnts = cmds.listRelatives( topJoint, c=1, f=1 )
    
    leftChild = ''
    rightChild = ''
    for child in childJnts:
        if cmds.xform( child, q=1, os=1, t=1 )[0] > 0:
            leftChild = child
        else:
            rightChild = child
    
    lfAnim = cmds.createNode( 'animCurveUA' )
    rfAnim = cmds.createNode( 'animCurveUA' )
    
    sgBFunction_attribute.addAttr( topJoint, ln='closeL', min=0, max=1, k=1 )
    sgBFunction_attribute.addAttr( topJoint, ln='closeR', min=0, max=1, k=1 )
    
    cmds.connectAttr( topJoint+'.closeL', lfAnim+'.input' )
    cmds.connectAttr( topJoint+'.closeR', rfAnim+'.input' )
    
    cmds.setKeyframe( lfAnim, f=0, v=0 )
    cmds.setKeyframe( lfAnim, f=1, v=closeValue )
    cmds.setKeyframe( rfAnim, f=0, v=0 )
    cmds.setKeyframe( rfAnim, f=1, v=closeValue )
    
    cmds.connectAttr( lfAnim+'.output', leftChild +'.rotateX' )
    cmds.connectAttr( rfAnim+'.output', rightChild+'.rotateX' )