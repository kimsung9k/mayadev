import maya.cmds as cmds



def createPointOnCurveNodes( curve, number ):
    
    crvShape = cmds.listRelatives( curve, s=1 )
    if not crvShape: return None
    crvShape = crvShape[0]
    
    nodes = []
    
    if number == 1:
        node = cmds.createNode( 'pointOnCurveInfo', n=curve+'_info0' )
        cmds.connectAttr( crvShape+'.local', node+'.inputCurve' )
        cmds.setAttr( node+'.top', 1 )
        cmds.setAttr( node+'.parameter', 0.5 )
        nodes.append( node )
    elif number > 1:
        eachRate = 1.0/(number-1)
        for i in range( number ):
            node = cmds.createNode( 'pointOnCurveInfo', n=curve+'_info0' )
            cmds.connectAttr( crvShape+'.local', node+'.inputCurve' )
            cmds.setAttr( node+'.top', 1 )
            cmds.setAttr( node+'.parameter',eachRate*i )
            nodes.append( node )
    
    return nodes




def createSplineNode( curve, number ):
    
    crvShape = cmds.listRelatives( curve, s=1 )
    if not crvShape: return None
    crvShape = crvShape[0]
    
    splineNode = cmds.createNode( 'splineCurveInfo', n=curve+'_spline' )
    cmds.connectAttr( crvShape+'.local', splineNode+'.inputCurve' )
    
    if number <= 1:
        return None
    elif number > 1:
        eachRate = 1.0/(number-1)
        for i in range( number ):
            cmds.setAttr( splineNode+'.parameter[%d]' % i, eachRate*i+0.001 )
    
    return splineNode




def ucCreatePointOnCurveNodes( number ):

    sels = cmds.ls( sl=1 )
    
    nodes = []
    for sel in sels:
        selShape = cmds.listRelatives( sel, s=1 )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'nurbsCurve': continue 
        nodes += createPointOnCurveNodes( sel, number )
    
    cmds.select( nodes )




def ucCreateSplineNode( number ):
    
    sels = cmds.ls( sl=1 )
    
    nodes = []
    for sel in sels:
        selShape = cmds.listRelatives( sel, s=1 )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'nurbsCurve': continue 
        nodes.append( createSplineNode( sel, number ) )
    
    cmds.select( nodes )