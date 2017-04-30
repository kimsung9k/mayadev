from sgModules import sgcommands

sels = cmds.ls( sl=1 )

points = sels[:-1]
mesh = sels[-1]

for point in points:
    sgcommands.createFollicleOnClosestPoint( point, mesh )