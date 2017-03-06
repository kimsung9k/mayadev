import math
import maya.OpenMaya as om
import maya.cmds as cmds
import sgModelConvert


def getMVectorFromTwoObj( objFirst, objSecond ):
    
    posFirst  = cmds.xform( objFirst,  q=1, ws=1, piv=1 )[:3]
    posSecond = cmds.xform( objSecond, q=1, ws=1, piv=1 )[:3]
    
    return om.MVector( *posSecond ) - om.MVector( *posFirst )



def getProjVector( vRay, vBase ):
    
    distRay = ( vRay * vBase )/( (vBase.x**2)+(vBase.y**2)+(vBase.z**2) )
    return vBase * distRay



def getVerticalVector( vRay, vBase ):
    
    vProj = getProjVector( vRay, vBase )
    
    return vRay - vProj


def getPoleVectorPosition( objTop, objMid, objEnd ):
    
    posTop = cmds.xform( objTop, q=1, ws=1, piv=1)[:3]
    posMid = cmds.xform( objMid, q=1, ws=1, piv=1)[:3]
    posEnd = cmds.xform( objEnd, q=1, ws=1, piv=1)[:3]
    
    vTopPos = om.MVector( *posTop )
    vMidPos = om.MVector( *posMid )
    vEndPos = om.MVector( *posEnd )
    
    vRay  = vMidPos - vTopPos
    vBase = vEndPos - vTopPos
    
    vVert = getVerticalVector( vRay, vBase )
    
    lengthVert = vVert.length()
    lengthBase = vBase.length()
    
    vnVert = vVert.normal()
    
    vPoleVector = vnVert * ( lengthVert + lengthBase )/2
    
    return vMidPos + vPoleVector


def getMatrix( vFirst, vSecond, vThird, pPoint ):
    
    vFirst  = sgModelConvert.convertMVector( vFirst )
    vSecond = sgModelConvert.convertMVector( vSecond )
    vThird  = sgModelConvert.convertMVector( vThird )
    pPoint  = sgModelConvert.convertMPoint( pPoint )
    
    return [ vFirst.x, vFirst.y, vFirst.z, 0,
             vSecond.x, vSecond.y, vSecond.z, 0,
             vThird.x, vThird.y, vThird.z, 0,
             pPoint.x, pPoint.y, pPoint.z, 1 ]