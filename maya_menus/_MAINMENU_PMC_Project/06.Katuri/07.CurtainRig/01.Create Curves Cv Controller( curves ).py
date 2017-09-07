from sgMaya import sgCmds, sgModel
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    selIndex = sels.index( sel )
    cvs = pymel.core.ls( sel + '.cv[*]', fl=1 )
    for cv in cvs:
        pos = pymel.core.xform( cv, q=1, ws=1, t=1 )[:3]
        ctl = sgCmds.makeController( sgModel.Controller.spherePoints, 1, makeParent=1, n='Ctl_detail_%d_%d' %( selIndex, cv.index() ) )
        ctlP = ctl.getParent()
        ctlP.t.set( pos )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        ctl.wm >> dcmp.imat
        dcmp.ot >> sel.getShape().attr( 'controlPoints[%d]' % cv.index() )