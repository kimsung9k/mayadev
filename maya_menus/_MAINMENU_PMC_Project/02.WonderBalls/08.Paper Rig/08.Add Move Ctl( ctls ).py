import pymel.core
from sgMaya import sgCmds, sgModel
sels = pymel.core.ls( sl=1 )
newCtls = []
for sel in sels:
    subCtl = sel.message.listConnections( s=0, d=1, p=1 )[0]
    mm = subCtl.node().wm.listConnections( s=0, d=1, type='multMatrix' )[0]
    dcmp = mm.o.listConnections( s=0, d=1, type='decomposeMatrix' )[0]
    jnt = dcmp.listConnections( s=0, d=1, type='transform' )[0]
    moveSubCtl = pymel.core.createNode( 'transform' )
    moveSubCtl.setParent( subCtl.node() )
    sgCmds.setTransformDefault( moveSubCtl )
    moveCtl = sgCmds.makeController( sgModel.Controller.pinPoints, 2, makeParent=1, n=sel + '_Move' )
    moveCtl.t >> moveSubCtl.t
    moveCtl.r >> moveSubCtl.r
    moveCtl.s >> moveSubCtl.s
    moveCtl.getParent().setParent( sel )
    sgCmds.setTransformDefault( moveCtl.getParent() )
    newCtls.append( moveCtl )
    pymel.core.delete( dcmp )
    sgCmds.constrain( moveSubCtl, jnt, ct=1, cr=1, cs=1, csh=1)
    
pymel.core.select( newCtls )