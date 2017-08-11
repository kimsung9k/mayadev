from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

ctl = sels[0]
ctlGrp = sels[1]

sgCmds.addAttr( ctl, ln='showDetail', min=0, max=1, at='long', cb=1 )
ctl.showDetail >> ctlGrp.v