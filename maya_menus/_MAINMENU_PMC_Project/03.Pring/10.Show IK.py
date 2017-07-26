import pymel.core

blCtls = pymel.core.ls( 'Ctl_Bl*_*_02', type='transform' )

for blCtl in blCtls:
    blCtl.blend.set( 0 )