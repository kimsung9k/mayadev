from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

ctls = sels[:-1]
curve = sels[-1]

sgCmds.createDetachCurve( ctls, curve )