from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

rotvalue = sels[-1].rotate.get()[0]
for sel in sels[:-1]:
    sel.setOrient( *rotvalue, ws=1 )