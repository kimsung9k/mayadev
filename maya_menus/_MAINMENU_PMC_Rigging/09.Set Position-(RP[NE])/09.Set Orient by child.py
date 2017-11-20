from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    children = sel.listRelatives( c=1, type='transform' )
    if not children: continue
    sgCmds.lookAt( children[0], sel, pcp=1 )