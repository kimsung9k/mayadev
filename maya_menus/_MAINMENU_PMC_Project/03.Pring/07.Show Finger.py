import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( 'Ctl_Finger_*_', type='transform' )
for sel in sels:
    sel.showDetail.set( 1 )