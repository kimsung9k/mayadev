from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( 'Ctl_*', type='transform' )

for sel in sels:
    if not sel.getShape(): continue
    sgCmds.renameShape( sel )
    if not sel.getParent().nodeName()[:3] == 'Ctl':
        sgCmds.renameParent( sel )