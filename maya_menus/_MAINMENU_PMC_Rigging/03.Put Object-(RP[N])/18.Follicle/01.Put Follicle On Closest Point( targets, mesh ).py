from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

points = sels[:-1]
mesh = sels[-1]

for point in points:
    sgCmds.createFollicleOnClosestPoint( point, mesh )