import maya.cmds as cmds

def createMiddleJoint( target ):
    
    cmds.select( target )
    newJnt = cmds.joint()
    cmds.setAttr( newJnt + '.radius', cmds.getAttr( target + '.radius' ) * 1.3 )
    
    compose = cmds.createNode( 'composeMatrix' )
    addMtx = cmds.createNode( 'addMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( compose + '.outputMatrix', addMtx + '.i[0]' )
    cmds.connectAttr( target + '.inverseMatrix', addMtx + '.i[1]' )
    cmds.connectAttr( addMtx + '.matrixSum', dcmp + '.imat' )
    
    cmds.connectAttr( dcmp + '.or', newJnt + '.r' )
    return newJnt

sels = cmds.ls( sl=1 )
middleJnts = []
for sel in sels:
    middleJnt = createMiddleJoint( sel )
    middleJnts.append( middleJnt )
cmds.select( middleJnts )