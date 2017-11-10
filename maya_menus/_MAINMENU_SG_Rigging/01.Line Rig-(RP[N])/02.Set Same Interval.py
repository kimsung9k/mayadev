import pymel.core
from sgMaya import sgCmds
from maya import OpenMaya

sels = pymel.core.ls( sl=1 )

srcPos = OpenMaya.MPoint( *pymel.core.xform( sels[-1], q=1, ws=1, t=1 ) )
dstMtx = sgCmds.listToMatrix( pymel.core.xform( sels[0], q=1, ws=1, matrix=1 ) )

localPos = srcPos * dstMtx.inverse()

lenSels = len( sels )
eachDist = localPos / ( lenSels-1 )

for i in range( 1, len( sels )-1 ):
    pos = ( eachDist * i ) * dstMtx
    pymel.core.xform( sels[i], ws=1, t= [  pos.x, pos.y, pos.z ] )