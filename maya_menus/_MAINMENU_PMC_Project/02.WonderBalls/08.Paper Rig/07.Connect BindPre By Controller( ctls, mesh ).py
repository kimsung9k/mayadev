import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )
targetMesh = sels[-1]

for sel in sels[:-1]:
    mm = sel.listConnections( s=0, d=1, type='multMatrix' )
    if not mm:
        moveCtl = pymel.core.ls( sel + '_Move' )[0]
        mm = moveCtl.listConnections( s=0, d=1, type='multMatrix' )
    
    jnt = mm[0].i[1].listConnections( s=1, d=0, type='joint' )[0]
    selP = sel.getParent()
    dcmp = selP.listConnections( s=1, d=0, type='decomposeMatrix' )[0]
    mm = dcmp.listConnections( s=1, d=0, type='multMatrix' )[0]
    bindPreObj = mm.i[0].listConnections( s=1, d=0 )[0]
    bindPreObj.rename( jnt + '_bindPre' )
    
    pymel.core.xform( bindPreObj, ws=1, matrix= jnt.wm.get() )
    
    sgCmds.connectBindPreMatrix( jnt, bindPreObj, targetMesh )
pymel.core.select( sels )