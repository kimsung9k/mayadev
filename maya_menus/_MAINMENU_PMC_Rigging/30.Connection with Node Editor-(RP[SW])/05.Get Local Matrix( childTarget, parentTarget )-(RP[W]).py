from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
node = sgCmds.getLocalMatrix( sels[0].wm, sels[1].wim )
pymel.core.select( node )