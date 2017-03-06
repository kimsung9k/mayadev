from sgModules import sgcommands


sels = sgcommands.listNodes( sl=1 )

for sel in sels:
    children = sel.listRelatives( c=1 )
    if not children: continue
    sgcommands.lookAt( children[0], sel, pcp=1 )