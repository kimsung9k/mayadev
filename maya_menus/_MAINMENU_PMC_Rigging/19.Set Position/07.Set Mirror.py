from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

for sel in sels:
    sgcommands.setMirrorLocal( sel )