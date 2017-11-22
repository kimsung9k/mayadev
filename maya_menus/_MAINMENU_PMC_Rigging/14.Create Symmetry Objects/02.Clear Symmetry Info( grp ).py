import pymel.core
from sgMaya import sgCmds
sels = pymel.core.listRelatives( , c=1, ad=1, type='transform' )
sels += pymel.core.ls( sl=1 )

for sel in sels:
    sgCmds.deleteAttr( sel, 'mirrorH' )