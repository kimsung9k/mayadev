import pymel.core
sels = pymel.core.ls( sl=1 )
jnts = pymel.core.listRelatives( sels, c=1, ad=1, type='joint' )
for jnt in jnts:
    jnt.radius.set( 0.5 )