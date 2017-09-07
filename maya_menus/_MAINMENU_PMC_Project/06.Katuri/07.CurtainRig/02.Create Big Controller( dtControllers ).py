from sgMaya import sgCmds, sgModel
import pymel.core
sels = pymel.core.ls( sl=1 )
ctls = []
for sel in sels:
    ctlCurtain = sgCmds.makeController( sgModel.Controller.spherePoints, 1, makeParent=1,
                           n = sel.replace( 'detail', 'Curtain' ) )
    pymel.core.xform( ctlCurtain.getParent(), ws=1, matrix= sel.wm.get() )
    ctls.append( ctlCurtain )

pymel.core.select( ctls )