import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

bezierCurve = pymel.core.curve( bezier=1, d=3, p=[ [0,0,0] for i in range( len( sels ) ) ] )
curveShape = bezierCurve.getShape()

for i in range( len( sels ) ):
    dcmp = sgCmds.getLocalDecomposeMatrix( sels[i].wm, bezierCurve.wim )
    dcmp.ot >> curveShape.controlPoints[i]