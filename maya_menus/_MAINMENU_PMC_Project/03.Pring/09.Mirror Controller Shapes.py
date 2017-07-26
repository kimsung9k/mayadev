import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( 'Ctl_Fk*_L_*', type='transform' )

for sel in sels:
    sgCmds.mirrorControllerShape(sel)