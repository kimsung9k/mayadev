from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( 'Ctl_*', type='transform' )

for sel in sels:
    sgCmds.renameShape( sel )
    if not sel.getParent()[:3] == 'Ctl':
        sgCmds.renameParent( sel )