import maya.cmds as cmds
import maya.OpenMaya as om
import sgModel3dMath

def printVector( vValue ):
    
    print vValue.x, vValue.y, vValue.z


def createBase( objTop, objMid, objEnd, objPoleV=None ):
    
    if not objPoleV:
        vPoleVPos = sgModel3dMath.getPoleVectorPosition( objTop, objMid, objEnd )
        objPoleV = cmds.createNode( 'transform', n= objTop+'_poleV' )
        cmds.setAttr( objPoleV+'.t', vPoleVPos.x, vPoleVPos.y, vPoleVPos.z )
        cmds.setAttr( objPoleV+'.dh', 1 )    
    
    vZDirection = om.MVector( 0, 0, 1 )
    
    vEnd   = sgModel3dMath.getMVectorFromTwoObj( objTop, objEnd )
    vMid   = sgModel3dMath.getMVectorFromTwoObj( objTop, objMid )
    vPoleV = sgModel3dMath.getMVectorFromTwoObj( objTop, objPoleV )
    
    midVerticalLength = sgModel3dMath.getVerticalVector(vMid, vEnd).length()
    vVertical = sgModel3dMath.getVerticalVector( vPoleV, vEnd ).normal() * midVerticalLength
    vProj     = sgModel3dMath.getProjVector( vMid, vEnd )
    vMid      = vVertical + vProj
    
    posTop = cmds.xform( objTop, q=1, ws=1, piv=1)[:3]
    posEnd = cmds.xform( objEnd, q=1, ws=1, piv=1)[:3]
    posMid = [posTop[0] + vMid.x, posTop[1] + vMid.y, posTop[2] + vMid.z]
    
    vEndFromMid = om.MVector( *posEnd ) - om.MVector( *posMid )
    
    if vZDirection * vPoleV < 0:
        vUp = vEnd ^ vPoleV
    else:
        vUp = vPoleV ^ vEnd
    
    vCrossTop = vMid ^ vUp
    vCrossMid = vEndFromMid ^ vUp
    
    vMid.normalize()
    vUp.normalize()
    vCrossTop.normalize()
    vCrossMid.normalize()
    vEndFromMid.normalize()
    
    if posTop[0] > 0:
        mtxTop = sgModel3dMath.getMatrix( vMid, vUp, vCrossTop, posTop )
        mtxMid = sgModel3dMath.getMatrix( vEndFromMid, vUp, vCrossMid, posMid )
        mtxEnd = sgModel3dMath.getMatrix( vEndFromMid, vUp, vCrossMid, posEnd )
    else:
        mtxTop = sgModel3dMath.getMatrix( -vMid, vUp, -vCrossTop, posTop )
        mtxMid = sgModel3dMath.getMatrix( -vEndFromMid, vUp, -vCrossMid, posMid )
        mtxEnd = sgModel3dMath.getMatrix( -vEndFromMid, vUp, -vCrossMid, posEnd )

    jntTop = cmds.createNode( 'joint' )
    jntMid = cmds.createNode( 'joint' )
    jntEnd = cmds.createNode( 'joint' )
    
    cmds.parent( jntEnd, jntMid )
    cmds.parent( jntMid, jntTop )
    
    cmds.xform( jntTop, ws=1, matrix=mtxTop )
    cmds.xform( jntMid, ws=1, matrix=mtxMid )
    cmds.xform( jntEnd, ws=1, matrix=mtxEnd )