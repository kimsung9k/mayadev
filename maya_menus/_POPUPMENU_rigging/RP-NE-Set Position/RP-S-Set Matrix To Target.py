from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

selPos = sels[-1].wm.get()
for sel in sels[:-1]:
    sel.xform( ws=1, matrix=selPos )