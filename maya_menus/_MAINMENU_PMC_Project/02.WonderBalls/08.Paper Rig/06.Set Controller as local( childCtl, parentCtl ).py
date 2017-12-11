from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

ctlChild = sels[0]
ctlTarget = sels[1]

pCtlChild = ctlChild.getParent()
pCtlTarget = ctlTarget.getParent()

dcmpChild = pCtlChild.listConnections( s=1, d=0, type='decomposeMatrix' )[0]
mChild = dcmpChild.listConnections( s=1, d=0, type='multMatrix' )[0]
dcmpTarget = pCtlTarget.listConnections( s=1, d=0, type='decomposeMatrix' )[0]
mTarget = dcmpTarget.listConnections( s=1, d=0, type='multMatrix' )[0]

trChild = mChild.i[0].listConnections( s=1, d=0 )[0]
trTarget = mTarget.i[0].listConnections( s=1, d=0 )[0]

localDcmp = sgCmds.getLocalDecomposeMatrix( trChild.wm, trTarget.wim )
trChildLocal = pymel.core.createNode( 'transform' )
trChildLocal.setParent( ctlTarget )
localDcmp.ot >> trChildLocal.t
localDcmp.outputRotate >> trChildLocal.r

pymel.core.delete( dcmpChild )
sgCmds.constrain( trChildLocal, pCtlChild, ct=1, cr=1, cs=1, csh=1 )