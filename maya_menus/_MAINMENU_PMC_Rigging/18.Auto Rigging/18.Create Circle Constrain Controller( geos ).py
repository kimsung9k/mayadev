from sgMaya import sgCmds, sgModel
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    bb = pymel.core.exactWorldBoundingBox( sel )
    bbmin = bb[:3]
    bbmax = bb[-3:]
    
    xLength = bbmax[0] - bbmin[0]
    zLength = bbmax[2] - bbmin[2]
    
    bbc = [ (bbmin[i] + bbmax[i])/2.0 for i in range( 3 ) ]
    
    maxLength = max( [xLength,zLength] )
    
    ctl = sgCmds.makeController( sgModel.Controller.circlePoints, maxLength/2.0*1.2, makeParent=1 )
    ctl.getParent().t.set( bbc )
    ctl.rename( 'Ctl_%s' % sel.name() )
    sgCmds.setIndexColor( ctl, 29 )
    
    sgCmds.setGeometryMatrixToTarget( sel, ctl )
    sgCmds.constrain( ctl, sel, ct=1, cr=1, cs=1, csh=1 )