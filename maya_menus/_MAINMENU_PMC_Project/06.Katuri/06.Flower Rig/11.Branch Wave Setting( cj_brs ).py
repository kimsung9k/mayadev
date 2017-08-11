from sgMaya import sgCmds, sgAnim
import pymel.core
sels = pymel.core.ls( sl=1 )

ctls = []

for topJoint in sels:
    mm = topJoint.listConnections( s=0, d=1, type='multMatrix' )[0]
    dcmp = mm.listConnections( s=0, d=1, type='decomposeMatrix' )[0]
    tr = dcmp.listConnections( s=0, d=1, type='transform' )[0]
    ctl = tr.listRelatives( c=1 )[0]
    sgAnim.makeWaveJoint( topJoint )
    
    sgAnim.makeUdAttrGlobal( [topJoint], ctl )
    
    ctl.allRandWeight.set( .2 )
    ctl.allRandBigSpeed.set( .3 )
    
    ctl.valueSineX.set( 1 )
    ctl.valueSineY.set( 3 )
    ctl.valueRandX.set( 1 )
    ctl.valueRandY.set( 3 )
    ctl.valueRandBigX.set( 1 )
    ctl.valueRandBigY.set( .5 )
    ctl.intervalValueAdd.set(30)
    
    sgCmds.setAttrCurrentAsDefault( ctl )
    ctls.append( ctl )

pymel.core.select( ctls )