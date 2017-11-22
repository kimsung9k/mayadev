import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

def makeWorldJointController( inputTargetCtl ):
    targetCtl = pymel.core.ls( inputTargetCtl )[0]
    ctlShapes = targetCtl.listRelatives( s=1 )
    targetCtlP = targetCtl.getParent()
    ctlChildren = targetCtl.listRelatives( c=1, type='transform' )
    mtx = targetCtl.wm.get()
    pymel.core.select( targetCtlP )
    jnt = pymel.core.joint()
    jnt.drawStyle.set( 2 )
    pymel.core.parent( ctlChildren, jnt )
    jnt.jo.set( sgCmds.getRotateFromMatrix( mtx ) )
    pymel.core.rotate( targetCtlP, 0,0,0, ws=1 )
    for ctlShape in ctlShapes:
        pymel.core.parent( ctlShape, jnt, add=1, shape=1 )
    targetCtlName = targetCtl.name()
    pymel.core.delete( targetCtl )
    jnt.rename( targetCtlName )
    return jnt

newCtls = []
for sel in sels:
    newCtl = makeWorldJointController( sel )
    newCtls.append( newCtl )
pymel.core.select( newCtls )