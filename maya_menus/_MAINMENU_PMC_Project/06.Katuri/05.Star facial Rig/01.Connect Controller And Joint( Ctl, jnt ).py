import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

ctl = sels[0]
jnt = sels[1]

ctlBase = ctl.getParent().getParent()

dcmp = sgCmds.getLocalDecomposeMatrix( ctl.wm, ctlBase.wim )
dcmp.ot >> jnt.t
dcmp.outputRotate >> jnt.r

ctl.rename( ctl.replace( 'sub_', '' ) )

