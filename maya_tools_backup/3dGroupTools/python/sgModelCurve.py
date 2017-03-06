import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDag
import sgModelData
import sgModelConvert


def getStartCurveMatrix( curve, aimIndex=0 ):
    
    startPoint = cmds.xform( curve+'.cv[0]', q=1, ws=1, t=1 )
    nextPoint  = cmds.xform( curve+'.cv[1]', q=1, ws=1, t=1 )
    
    aimIndex   = (aimIndex+3) % 3
    upIndex    = (aimIndex+4) % 3
    crossIndex = (aimIndex+5) % 3
    
    lAim = [nextPoint[0] - startPoint[0],nextPoint[1] - startPoint[1], nextPoint[2] - startPoint[2]]
    lUp = [0,0,0]
    lUp[ aimIndex ] = -lAim[ upIndex ]
    lUp[ upIndex ]  = lAim[ aimIndex ]
    vAim = om.MVector( *lAim )
    vUp  = om.MVector( *lUp )
    vCross = vAim^vUp
    vUp = vCross ^ vAim
    
    vAim.normalize()
    vUp.normalize()
    vCross.normalize()
    
    mtx = [ int(i%5 == 0) for i in range( 16 ) ]
    
    mtx[ aimIndex*4 + 0 ] = vAim.x
    mtx[ aimIndex*4 + 1 ] = vAim.y
    mtx[ aimIndex*4 + 2 ] = vAim.z
    
    mtx[ upIndex*4 + 0 ] = vUp.x
    mtx[ upIndex*4 + 1 ] = vUp.y
    mtx[ upIndex*4 + 2 ] = vUp.z
    
    mtx[ crossIndex*4 + 0 ] = vCross.x
    mtx[ crossIndex*4 + 1 ] = vCross.y
    mtx[ crossIndex*4 + 2 ] = vCross.z
    
    mtx[ 3*4 + 0 ] = startPoint[0]
    mtx[ 3*4 + 1 ] = startPoint[1]
    mtx[ 3*4 + 2 ] = startPoint[2]
    
    return mtx



def getSourceCurveAttr( shape ):
    
    cons = cmds.listConnections( shape+'.create', s=1, d=0, p=1, c=1 )
    shapeP = cmds.listRelatives( shape, p=1 )[0]
    
    if not cons:
        
        duObj = cmds.duplicate( shape )[0]
        duShapes = cmds.listRelatives( duObj, s=1, f=1 )
        
        targetOrig = ''
        for duShape in duShapes:
            if not cmds.getAttr( duShape+'.io' ):
                targetOrig = duShape
                break
        
        cmds.setAttr( targetOrig+'.io', 1 )
        targetOrig = cmds.parent( targetOrig, shapeP, s=1, add=1 )[0]
        
        cmds.delete( duObj )
        
        cons = cmds.listConnections( shape+'.controlPoints', p=1, c=1, s=1, d=0 )
        if cons:
            for i in range( 0, len( cons ), 2 ):
                cmds.connectAttr( cons[i+1], cons[i].replace( shape, targetOrig ) )
                cmds.disconnectAttr( cons[i+1], cons[i] )
            
        return targetOrig+'.local'
        
    else:
        return cons[1]



def getPointAtParam( curve, paramValue, **options ):
    
    curveShape = sgModelDag.getShape( curve )
    
    objectSpace = sgModelData.getValueFromDict( options, 'os' )
    
    fnCurve= om.MFnNurbsCurve( sgModelDag.getDagPath( curveShape ) )
    
    pointValue = om.MPoint()
    if objectSpace:
        fnCurve.getPointAtParam( paramValue, pointValue )
    else:
        worldMatrix = cmds.getAttr( curve+'.wm')
        worldMMatrix = sgModelConvert.convertMatrixToMMatrix( worldMatrix )
        fnCurve.getPointAtParam( paramValue, pointValue )
        pointValue *= worldMMatrix

    return pointValue




def getParamAtPoint( curve, MPointValue, **options ):
    
    curveShape = sgModelDag.getShape( curve )
    
    objectSpace = sgModelData.getValueFromDict( options, 'os' )
    
    nearPointOnCurve = cmds.createNode( 'nearestPointOnCurve')
    cmds.connectAttr( curveShape+'.local', nearPointOnCurve+'.inputCurve' )
    
    paramValue = 0.0
    if objectSpace:
        cmds.setAttr( nearPointOnCurve+'.inPosition', MPointValue.x, MPointValue.y, MPointValue.z )
        paramValue = cmds.getAttr( nearPointOnCurve+'.parameter' )
    else:
        worldMatrix = cmds.getAttr( curve+'.wm')
        worldMMatrix = sgModelConvert.convertMatrixToMMatrix( worldMatrix )
        localMPoint = MPointValue * worldMMatrix.inverse()
        cmds.setAttr( nearPointOnCurve+'.inPosition', localMPoint.x, localMPoint.y, localMPoint.z )
        paramValue = cmds.getAttr( nearPointOnCurve+'.parameter' )
    
    cmds.delete( nearPointOnCurve )
    return paramValue




def getTangentAtParam( curve, paramValue, **options ):
    
    curveShape = sgModelDag.getShape( curve )
    
    objectSpace = sgModelData.getValueFromDict( options, 'os' )
    
    fnCurve= om.MFnNurbsCurve( sgModelDag.getDagPath( curveShape ) )
    
    tangentValue = om.MVector()
    if objectSpace:
        tangentValue = fnCurve.tangent( paramValue )
    else:
        worldMatrix = cmds.getAttr( curve+'.wm')
        worldMMatrix = sgModelConvert.convertMatrixToMMatrix( worldMatrix )
        tangentValue = fnCurve.tangent( paramValue ) * worldMMatrix
    
    return tangentValue