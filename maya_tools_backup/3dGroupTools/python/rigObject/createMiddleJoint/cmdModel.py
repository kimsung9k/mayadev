import maya.cmds as cmds


def createMiddleJoint( targetJoint, offset ):
    
    jointParent = cmds.listRelatives( targetJoint, p=1 )
    
    if not jointParent: return None
    
    blMtx = cmds.createNode( 'blendTwoMatrix' )
    mtxToTbT = cmds.createNode( 'matrixToThreeByThree' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    mtOfx = cmds.createNode( 'multiplyDivide' )
    mtOfy = cmds.createNode( 'multiplyDivide' )
    mtOfz = cmds.createNode( 'multiplyDivide' )
    average = cmds.createNode( 'plusMinusAverage' )
    
    cmds.select( targetJoint )
    middleJnt = cmds.joint()
    
    cmds.addAttr( middleJnt, ln='offsetX', dv=offset[0] )
    cmds.addAttr( middleJnt, ln='offsetY', dv=offset[1] )
    cmds.addAttr( middleJnt, ln='offsetZ', dv=offset[2] )
    cmds.setAttr( middleJnt+'.offsetX', e=1, k=1 )
    cmds.setAttr( middleJnt+'.offsetY', e=1, k=1 )
    cmds.setAttr( middleJnt+'.offsetZ', e=1, k=1 )
    
    cmds.connectAttr( targetJoint+'.im', blMtx+'.inMatrix1' )
    cmds.connectAttr( blMtx+'.outMatrix', mtxToTbT+'.inMatrix' )
    cmds.connectAttr( mtxToTbT+'.out00', mtOfx+'.input1X' )
    cmds.connectAttr( mtxToTbT+'.out01', mtOfx+'.input1Y' )
    cmds.connectAttr( mtxToTbT+'.out02', mtOfx+'.input1Z' )
    cmds.connectAttr( mtxToTbT+'.out10', mtOfy+'.input1X' )
    cmds.connectAttr( mtxToTbT+'.out11', mtOfy+'.input1Y' )
    cmds.connectAttr( mtxToTbT+'.out12', mtOfy+'.input1Z' )
    cmds.connectAttr( mtxToTbT+'.out20', mtOfz+'.input1X' )
    cmds.connectAttr( mtxToTbT+'.out21', mtOfz+'.input1Y' )
    cmds.connectAttr( mtxToTbT+'.out22', mtOfz+'.input1Z' )
    cmds.connectAttr( middleJnt+'.offsetX', mtOfx+'.input2X' )
    cmds.connectAttr( middleJnt+'.offsetX', mtOfx+'.input2Y' )
    cmds.connectAttr( middleJnt+'.offsetX', mtOfx+'.input2Z' )
    cmds.connectAttr( middleJnt+'.offsetY', mtOfy+'.input2X' )
    cmds.connectAttr( middleJnt+'.offsetY', mtOfy+'.input2Y' )
    cmds.connectAttr( middleJnt+'.offsetY', mtOfy+'.input2Z' )
    cmds.connectAttr( middleJnt+'.offsetZ', mtOfz+'.input2X' )
    cmds.connectAttr( middleJnt+'.offsetZ', mtOfz+'.input2Y' )
    cmds.connectAttr( middleJnt+'.offsetZ', mtOfz+'.input2Z' )
    
    cmds.connectAttr( mtOfx+'.output', average+'.input3D[0]' )
    cmds.connectAttr( mtOfy+'.output', average+'.input3D[1]' )
    cmds.connectAttr( mtOfz+'.output', average+'.input3D[2]' )
    
    cmds.connectAttr( average+'.output3D', middleJnt+'.t' )
    cmds.connectAttr( blMtx+'.outMatrix', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.or', middleJnt+'.jo' )
    
    

def uiCmd_createMiddleJoint( offset, *args ):
    
    selections = cmds.ls( sl=1 )
    
    for selection in selections:
        createMiddleJoint( selection, offset )