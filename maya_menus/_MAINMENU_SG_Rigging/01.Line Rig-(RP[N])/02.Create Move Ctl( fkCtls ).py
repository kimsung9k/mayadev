from sgMaya import sgCmds, sgModel
import pymel.core

sels = pymel.core.ls( sl=1 )

for sel in sels:
    bb = pymel.core.exactWorldBoundingBox( sel.getShape() )
    xDist = bb[3]-bb[0]
    yDist = bb[4]-bb[1]
    zDist = bb[5]-bb[2]
    size = max( xDist, yDist, zDist )
    
    moveCtl = sgCmds.makeController( sgModel.Controller.pinPoints, size / 1.5, makeParent=1 )
    if xDist == size: moveCtl.getShape()
    moveCtl.rename( sel + '_move' )
    moveCtl.getParent().setParent( sel )
    sgCmds.setTransformDefault( moveCtl.getParent() )