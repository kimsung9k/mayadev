from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

for sel in sels[2:]:
    sgcommands.constrain_tangent( sels[0], sels[1], sel )