from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    mirrorTransform = sgCmds.makeMirrorTransform( sel )
    mirrorTransform.setParent( sel.getParent() )