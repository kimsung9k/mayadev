import pymel.core
from sgMaya import sgAnim

sels = pymel.core.ls( sl=1 )

topJoints = sels[:-1]
ctl = sels[-1]

targetPCtls = []
for topJoint in topJoints:
    sgAnim.makeWaveJoint( topJoint )
    mm = topJoint.listConnections( s=0, d=1, type='multMatrix' )[0]
    dcmp = mm.listConnections( s=0, d=1, type='decomposeMatrix' )[0]
    tr = dcmp.listConnections( s=0, d=1, type='transform' )[0]
    targetPCtls.append( tr )
    
sgAnim.makeWaveGlobal( topJoints, ctl )

ctl.allRandWeight.set( .2 )
ctl.allRandBigSpeed.set( .3 )

ctl.valueSineX.set( 1 )
ctl.valueSineY.set( .5 )
ctl.valueRandX.set( 1 )
ctl.valueRandY.set( .5 )
ctl.valueRandBigX.set( 1 )
ctl.valueRandBigY.set( .5 )
ctl.offsetGlobalInterval.set(0.0)
ctl.offsetGlobalRand.set(0.15)
ctl.intervalValueAdd.set(30)