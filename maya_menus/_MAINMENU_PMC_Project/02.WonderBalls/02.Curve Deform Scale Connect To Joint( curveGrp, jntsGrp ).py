from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

curveGrp = sels[0]
jntGrp = sels[1]
targets = jntGrp.listRelatives( c=1 )

for curve in curveGrp.listRelatives( c=1 ):
    curveShape, curveOrigShape = curve.listRelatives( s=1 )
    for target in targets:
        sgCmds.connectCurveScale( curveOrigShape.local, curveShape.local, target )