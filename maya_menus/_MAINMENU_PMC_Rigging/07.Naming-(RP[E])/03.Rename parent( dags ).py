from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
for sel in sels:
    selP = sel.parent()
    if not selP: continue
    selP.rename( 'P' + sel.localName() )