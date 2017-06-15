from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

ctls = sels[:-1]
target = sels[-1]

sgCmds.duplicateBlendShapeByCtl( ctls, target )