from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
targets = sels[:-1]
mesh = sels[-1]
for target in targets:
    sgCmds.bindTransformToMesh( target, mesh, cr=0 )