from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

srcMesh = sels[0]
dstMesh = sels[1]

for hist in dstMesh.history():
    if hist.type() != 'mesh': continue
    if dstMesh != hist.getParent(): continue
    if not hist.io.get(): continue
    srcMesh.getShape().outMesh >> hist.inMesh