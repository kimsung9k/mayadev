from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( 'Ctl_*', type='transform' )

for sel in sels:
    sgCmds.unlockParent( sel )