from sgMaya import sgRig
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    sgRig.createSimplePlaneControl( sel )