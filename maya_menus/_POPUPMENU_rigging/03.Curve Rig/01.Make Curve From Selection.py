from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
lenSels = len( sels )
if lenSels < 3:
    degree = 1
elif lenSels == 3:
    degree = 2
else:
    degree = 3
sgcommands.makeCurveFromSelection( sels, d=degree )