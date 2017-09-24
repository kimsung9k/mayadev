from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

for sel in sels:
    
    poleVConst = sel.t.listConnections( s=0, d=1, type='poleVectorConstraint' )[0]
    
    ikHandle = poleVConst.constraintTranslateX.listConnections( s=0, d=1, type='ikHandle' )[0]
    
    endEffector = ikHandle.endEffector.listConnections( s=1, d=0 )[0]
    
    endJnt = endEffector.tx.listConnections( s=1, d=0 )[0]
    middleJnt = endEffector.getParent()
    
    mdMiddle = middleJnt.tx.listConnections( s=1, d=0 )[0]
    mdEnd    = endJnt.tx.listConnections( s=1, d=0 )[0]
    
    sgCmds.addOptionAttribute( sel, 'IK Length' )
    sgCmds.addAttr( sel, ln='ikUpperLength', k=1 )
    sgCmds.addAttr( sel, ln='ikLowerLength', k=1 )
    
    powMiddle = pymel.core.createNode( 'multiplyDivide' )
    powMiddle.input1X.set( 2 ); powMiddle.op.set( 3 )
    powEnd = pymel.core.createNode( 'multiplyDivide' )
    powEnd.input1X.set( 2 ); powEnd.op.set( 3 )
    sel.attr( 'ikUpperLength' ) >> powMiddle.input2X
    sel.attr( 'ikLowerLength' ) >> powEnd.input2X
    
    origDistMiddle = mdMiddle.input2Y.get()
    origDistEnd    = mdEnd.input2Y.get()
    
    multMid = pymel.core.createNode( 'multDoubleLinear' )
    multEnd = pymel.core.createNode( 'multDoubleLinear' )
    
    multMid.input1.set( origDistMiddle )
    multEnd.input1.set( origDistEnd )
    powMiddle.outputX >> multMid.input2
    powEnd.outputX >> multEnd.input2
    
    multMid.output >> mdMiddle.input2Y
    multEnd.output >> mdEnd.input2Y

pymel.core.select( sels )
    