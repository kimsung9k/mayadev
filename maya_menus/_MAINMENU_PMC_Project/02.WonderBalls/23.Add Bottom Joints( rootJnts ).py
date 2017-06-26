import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

for sel in sels:
    cons = sel.listConnections( s=1, d=0 )
    dcmp = cons[0]
    mm = dcmp.listConnections( s=1, d=0 )[0]
    rootCtl = mm.listConnections( s=1, d=0 )[0]
    pymel.core.delete( dcmp )
    jntP = sel.getParent()
    pymel.core.select( jntP )
    bottomJoint = pymel.core.joint( n= 'bottom_joint_' + '_'.join( sel.split( '_' )[1:-1] ) )
    constObj = pymel.core.createNode( 'transform' )
    sgCmds.constrain_all( constObj, bottomJoint )
    constObj.setParent( rootCtl )
    sel.setParent( bottomJoint )
    sel.segmentScaleCompensate.set( 0 )