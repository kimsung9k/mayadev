import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

sel_0_p = sels[0].getParent()

dcmpChild  = sgCmds.getLocalDecomposeMatrix( sels[0].wm, sels[1].wim )
dcmpParent = sgCmds.getLocalDecomposeMatrix( sels[1].wm, sels[0].wim )

multNodeValue = [0,0,0]
multNodeValue[ dirIndex%3 ] = 0.25

trChild = pymel.core.createNode( 'transform' )
trParent = pymel.core.createNode( 'transform' )
trChild.rename( 'trChild' )
trParent.rename( 'trParent' )

multNodeChild = pymel.core.createNode( 'multiplyDivide' )
multNodeParent = pymel.core.createNode( 'multiplyDivide' )

dcmpChild.ot >> multNodeChild.input1; multNodeChild.input2.set( multNodeValue )
dcmpParent.ot >> multNodeParent.input1; multNodeParent.input2.set( multNodeValue )

multNodeChild.output >> trChild.t
multNodeParent.output >> trParent.t

trChild.dh.set( 1 )
trParent.dh.set( 1 )
trChildG = pymel.core.group( em=1 )
trParentG = pymel.core.group( em=1 )
trChild.setParent( trChildG )
trParent.setParent( trParentG )

pymel.core.parent( trChildG, sels[1] )
pymel.core.parent( trParentG, sels[0] )

sgCmds.setTransformDefault( trChildG )
sgCmds.setTransformDefault( trParentG )
sels[1].s >> trChildG.s
sels[0].s >> trParentG.s