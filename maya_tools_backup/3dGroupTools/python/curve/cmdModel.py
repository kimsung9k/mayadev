import maya.cmds as cmds
import basecode
import sgRigCurve

def uiCmd_createEpCurve( *args ):
    
    autoLoadPlugin = basecode.AutoLoadPlugin()
    autoLoadPlugin.load( 'epCurveNode' )
    
    selections = cmds.ls( sl=1 )
    
    epCurveNode = cmds.createNode( 'epCurveNode' )
    curveNode = cmds.createNode( 'nurbsCurve' )
    cmds.connectAttr( epCurveNode+'.outputCurve', curveNode+'.create' )
    
    for i in range( len( selections ) ):
        dcm = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( selections[i]+'.wm', dcm+'.imat' )
        cmds.connectAttr( dcm+'.ot', epCurveNode+'.inputPoint[%d]' % i )
        
        
        
        
def uiCmd_createSplineJointEachSpans( *args ):
    
    selections = cmds.ls( sl=1 )
    curve = selections[0]
    curveShape = cmds.listRelatives( curve, s=1 )[0]
    
    minValue = cmds.getAttr( curveShape+'.minValue' )
    maxValue = cmds.getAttr( curveShape+'.maxValue' )
    
    spans    = cmds.getAttr( curveShape+'.spans' )
    
    paramRange = maxValue - minValue
    eachParamRate = paramRange / spans
    
    infos = []
    
    for i in range( 0, spans+1 ):
        info = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( curveShape+'.local', info+'.inputCurve' )
        cmds.setAttr( info+'.parameter', eachParamRate*i )
        infos.append( info )
    
    cmds.select( d=1 )
    jnts = [ cmds.joint() ]
    for i in range( spans ):
        cmds.select( jnts[-1] )
        jnt = cmds.joint()
        jnts.append( jnt )
        
        distNode = cmds.createNode( 'distanceBetween' )
        cmds.connectAttr( infos[i]+'.position', distNode+'.point1' )
        cmds.connectAttr( infos[i+1]+'.position', distNode+'.point2' )
        cmds.connectAttr( distNode+'.distance', jnt+'.tx' )

    cmds.ikHandle( sj=jnts[0], ee=jnts[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=curveShape )



def createSgWobbleCurve( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        sgRigCurve.createSgWobbleCurve( sel, 0 )