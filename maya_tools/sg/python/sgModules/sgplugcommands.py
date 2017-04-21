import pymel.core


def sgControlledCurveSet( ctls, curve ):
    
    nearPointOnCurve = pymel.core.createNode( 'nearestPointOnCurve' )
    
    node = pymel.core.createNode( 'SGControlledCurve00' )
    
    curve = pymel.core.ls( curve )[0]
    curveShape = curve.getShape()
    
    curveShape.worldSpace >> nearPointOnCurve.inputCurve
    curveShape.worldSpace >> node.inputCurve
    
    newCurve = pymel.core.createNode( 'nurbsCurve' )
    node.outputCurve >> newCurve.create
    
    for i in range( len( ctls ) ):
        ctl = pymel.core.ls( ctls[i] )[0]
        ctlPos = pymel.core.xform( ctl, q=1, ws=1, t=1 )
        nearPointOnCurve.inPosition.set( ctlPos )
        paramValue = nearPointOnCurve.parameter.get()
        node.controls[i].parameter.set( paramValue )
        ctl.wm >> node.controls[i].matrix
        ctl.pim >> node.controls[i].bindPreMatrix
    
    pymel.core.delete( nearPointOnCurve )