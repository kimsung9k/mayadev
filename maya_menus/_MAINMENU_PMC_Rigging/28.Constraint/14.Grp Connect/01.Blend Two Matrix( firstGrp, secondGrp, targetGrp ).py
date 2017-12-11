import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

first = sels[0]
second = sels[1]
target   = sels[2]

sgCmds.addAttr( target, ln='blend', min=0, max=1, k=1 )

chFirsts = first.listRelatives( c=1, type='transform' )
chSeconds = second.listRelatives( c=1, type='transform' )
chTargets = target.listRelatives( c=1, type='transform' )

for i in range( len( chFirsts ) ):
    chFirst = chFirsts[i]
    chSecond = chSeconds[i]
    chTarget = chTargets[i]
    sgCmds.blendTwoMatrixConnect( chFirst, chSecond, chTarget, ct=1, cr=1 )
    target.attr( 'blend' ) >> chTarget.attr( 'blend' )