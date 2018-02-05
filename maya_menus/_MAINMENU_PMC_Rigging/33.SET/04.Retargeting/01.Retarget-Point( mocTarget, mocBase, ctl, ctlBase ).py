import pymel.core
sels = pymel.core.ls( sl=1 )

target = sels[0]
targetBase = sels[1]
ctl = sels[2]
ctlBase = sels[3]

multMtx = pymel.core.createNode( 'multMatrix' )
compose = pymel.core.createNode( 'composeMatrix' )
multNode = pymel.core.createNode( 'multiplyDivide' )
ctl.rotatePivot >> multNode.input1
multNode.input2.set( -1,-1,-1 )
multNode.output >> compose.it
compose.outputMatrix >> multMtx.i[0]
target.wm >> multMtx.i[1]
targetBase.wim >> multMtx.i[2]
ctlBase.wm >> multMtx.i[3]
ctl.pim >> multMtx.i[4]
dcmp = pymel.core.createNode( 'decomposeMatrix' )
multMtx.matrixSum >> dcmp.imat
dcmp.ot >> ctl.t