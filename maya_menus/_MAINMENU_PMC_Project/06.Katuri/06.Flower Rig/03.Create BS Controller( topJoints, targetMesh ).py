from sgMaya import sgCmds
import pymel.core

def renameParent( *targets ):
    for target in targets:
        target.getParent().rename( 'P' + target.shortName() )

sels = pymel.core.ls( sl=1 )
topGrp = sels[-1].getAllParents()[-1]

ctlTops = []
for i in range( len( sels )-1 ):
    topJoint = sels[i]
    ctls, pinCtls = sgCmds.createFkControl( topJoint, 1.0, 0 )
    for j in range( len( ctls ) ):
        ctls[j].rename( 'Ctl_' + topGrp + '_bs_%d_%d' % ( i, j ) )
        renameParent( ctls[j] )
        sgCmds.setIndexColor( ctls[j], 29 )
        
    ctlsTop = ctls[0].getAllParents()[0]
    ctlTops.append( ctlsTop )

grp = pymel.core.group( ctlTops )
grp.rename( 'CtlsGrp_bs_' + topGrp )