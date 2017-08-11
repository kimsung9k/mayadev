import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

transforms = sels[:-1]
mesh = sels[-1]

for tr in transforms:
    sgCmds.bindTransformToMesh( tr, mesh, cr=0 )