from sgMaya import sgCmds, sgModel

sels = pymel.core.ls( sl=1 )
geo = sels[0]
ctl = sels[1]

for i in range( 2 ):
    bendCtl = sgCmds.makeController( sgModel.Controller.switchPoints, 1, makeParent=1, name= ctl.replace( 'Part', 'Bend%d' % i ) )
    pBendCtl = bendCtl.getParent()
    
    bendCtl.getShape().shape_ty.set( 0.5 )
    bendCtl.getShape().shape_rx.set( 90 )
    
    pBendCtl.setParent( ctl )
    sgCmds.setTransformDefault( pBendCtl )
    pBendCtl.r.set( 0, 90*i, 0 )
    bend1, handle1 = pymel.core.nonLinear( geo, type='bend' )
    handle1.setParent( bendCtl )
    sgCmds.setTransformDefault( handle1 )
    handle1.r.set( 0,0,90 )
    bend1.lowBound.set( 0 )
    sgCmds.addOptionAttribute( bendCtl )
    sgCmds.addAttr( bendCtl, ln='bend', k=1 )
    multNode = pymel.core.createNode( 'multDoubleLinear' )
    bendCtl.bend >> multNode.input1
    multNode.input2.set( 5 )
    multNode.output >> bend1.curvature
    handle1.v.set( 0 )
    
    sgCmds.addAttr( bendCtl, ln='lowBound', k=1, min=0, dv=1 )
    sgCmds.addAttr( bendCtl, ln='highBound', k=1, min=0, dv=1 )
    multLow = pymel.core.createNode( 'multDoubleLinear' )
    bendCtl.lowBound >> multLow.input1
    multLow.input2.set( -1 )
    multLow.output >> bend1.lowBound
    bendCtl.highBound >> bend1.highBound