import pymel.core

allJnts = pymel.core.ls( 'jnts_*' )

for jnt in allJnts:
    if jnt.type() == 'transform':
        jnt.rename( jnt.name()[5:].capitalize() + '_jointGrp' )

for jntGrp in pymel.core.ls( '*_jointGrp', type='transform' ):
    childrenJnts = jntGrp.listRelatives( c=1, type='joint' )
    
    for i in range( len( childrenJnts ) ):
        childrenJnts[i].rename( 'temp' )
    
    for i in range( len( childrenJnts ) ):
        jntNameSplits = jntGrp.replace( 'Grp', '' ).split( '_' )
        jntNameSplits[0] += '%03d' % i
        childrenJnts[i].rename( '_'.join(jntNameSplits) )