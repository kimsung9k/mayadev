from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

targetObjs = sels[:-1]
curve = sels[-1]

for targetObj in targetObjs:
    sgCmds.attachToCurve( targetObj, curve )