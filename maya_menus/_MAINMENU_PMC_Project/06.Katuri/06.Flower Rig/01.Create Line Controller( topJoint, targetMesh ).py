from sgMaya import sgCmds
import pymel.core

def renameParent( *targets ):
    for target in targets:
        target.getParent().rename( 'P' + target.shortName() )

sels = pymel.core.ls( sl=1 )
topGrp = sels[1].getAllParents()[-1]

firstCtl, endCtl, middleCtl, eachCtls, ctlsGrp, etcGrp = sgCmds.createLineController( sels[0] )
firstCtl.shape_sy.set( 6 )
firstCtl.shape_sz.set( 6 )
endCtl.shape_sy.set( 6 )
endCtl.shape_sz.set( 6 )
middleCtl.scaleMult.set( 2 )

firstCtl.rename( 'Ctl_' + topGrp + '_Root00' )
middleCtl.rename( 'Ctl_' + topGrp + '_Root01' )
endCtl.rename( 'Ctl_' + topGrp + '_Root02' )
renameParent( firstCtl, middleCtl, endCtl )
ctlsGrp.rename( 'CtlsGrp_' + topGrp )
etcGrp.rename( 'EtcGrp_' + topGrp )

sgCmds.setIndexColor( firstCtl, 17 )
sgCmds.setIndexColor( middleCtl, 20 )
sgCmds.setIndexColor( endCtl, 17 )

for i in range( len( eachCtls ) ):
    eachCtl = eachCtls[i]
    sgCmds.setIndexColor( eachCtl, 10 )
    eachCtl.shape_sx.set( 2.4 )
    eachCtl.shape_sz.set( 2.4 )
    eachCtl.rename( 'Ctl_' + topGrp + '_RootDt%d' % i )
    renameParent( eachCtl )