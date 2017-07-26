import pymel.core
sels = pymel.core.ls( 'Ctl_Fk*_L_*', type='transform' )

for sel in sels:
    sel.shape_ry.set( 45 )