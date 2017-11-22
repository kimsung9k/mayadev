from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )
pointers = sels[:-1]
crv = sels[-1]

targets = []
for pointer in pointers:
    target = sgCmds.createNearestPointOnCurveObject( pointer, crv )
    targets.append( target )

pymel.core.select( targets )