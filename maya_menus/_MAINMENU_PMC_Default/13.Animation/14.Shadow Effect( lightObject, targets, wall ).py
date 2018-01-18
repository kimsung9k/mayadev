from sgMaya import sgCmds, sgRig
import pymel.core

sels = pymel.core.ls( sl=1 )

sgRig.shadowEffect( sels[0], sels[1:-1], sels[-1] )