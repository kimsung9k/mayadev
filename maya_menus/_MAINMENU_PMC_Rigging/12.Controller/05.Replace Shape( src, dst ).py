from sgModules import sgcommands
sels = sgcommands.listNodes( sl=1 )

for sel in sels[1:]:
    sgcommands.replaceShape( sels[0], sel )