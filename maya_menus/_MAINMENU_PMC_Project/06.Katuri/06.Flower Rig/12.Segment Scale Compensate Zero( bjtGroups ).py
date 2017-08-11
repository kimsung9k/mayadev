import pymel.core

sels = pymel.core.ls( sl=1 )
allJnts = []
for sel in sels:
    jnts = sel.listRelatives( c=1, ad=1, f=1, type='joint' )
    jnts.reverse()
    if sel.nodeType() == 'joint':
        jnts.append( sel )
    allJnts += jnts

for jnt in allJnts:
    jnt.segmentScaleCompensate.set( 0 )