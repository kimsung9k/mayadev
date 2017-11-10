import pymel.core


def makeParent( inputTopObject ):
    
    topObject = pymel.core.ls( inputTopObject )[0]
    posTopObject = topObject.wm.get()
    newTransform = pymel.core.createNode( 'transform', n='P'+topObject.nodeName() )
    pymel.core.xform( newTransform, ws=1, matrix=topObject.wm.get() )
    topObject.setParent( newTransform )
    return newTransform


def createCurveFromJointLine( inputTopJoint ):
    
    topJoint = pymel.core.ls( inputTopJoint )[0]
    jnts = topJoint.listRelatives( c=1, ad=1 )
    jnts.append( topJoint )
    jnts.reverse()    
    
    points = []
    for jnt in jnts:
        points.append( pymel.core.xform( jnt, q=1, ws=1, t=1 ) )

    return pymel.core.curve( ep=points, d=3 )



def connectIkSpline( inputTopJoint, inputCurve ):
    
    topJoint = pymel.core.ls( inputTopJoint )[0]
    curve = pymel.core.ls( inputCurve )[0]
    jnts = topJoint.listRelatives( c=1, ad=1 )
    endJnt = jnts[0]
    return pymel.core.ikHandle( sj=topJoint, ee=endJnt, curve=curve, solver='ikSplineSolver', ccv=False, pcv=False )



topJoints = pymel.core.ls( sl=1 )

pTopJoints = []
curves = []
handles = []

for topJoint in topJoints:
    pTopJoint = makeParent( topJoint )
    curve = createCurveFromJointLine( topJoint )
    ikHandle, ee = connectIkSpline( topJoint, curve )
    
    pTopJoints.append( pTopJoint )
    curves.append( curve )
    handles.append( ikHandle )

topJntsGrp = pymel.core.group( pTopJoints, n='topJointsGrp' )
curvesGrp = pymel.core.group( curves, n='curvesGrp' )
handlesGrp = pymel.core.group( handles, n='handlesGrp' )
handlesGrp.v.set( 0 )