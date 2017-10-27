from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

ctl = sels[0]
mod = sels[1]

sgCmds.addOptionAttribute( ctl )
sgCmds.addAttr( ctl, ln='modVis', k=1, min=0, max=1, dv=1, at='long' )
ctl.attr( 'modVis' ) >> mod.v