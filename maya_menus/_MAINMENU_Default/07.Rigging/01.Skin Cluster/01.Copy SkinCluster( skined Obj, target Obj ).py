from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

srcMesh = sels[0]
others = sels[1:]

for other in others:
    children = other.listRelatives( c=1, ad=1, type='transform' )
    children.append( other )
    trs = []
    for child in children:
        shape = child.shape()
        if not shape: continue
        trs.append( child )
    for tr in trs:
        sgcommands.autoCopyWeight( srcMesh, tr )