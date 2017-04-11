from sgModules import sgcommands

sels = cmds.ls( sl=1 )
children = cmds.listRelatives( sels, c=1, ad=1, type='transform' )
children += sels

meshs = []
for child in children:
    shapes = cmds.listRelatives( child, s=1, f=1 )
    if not shapes: continue
    meshExists = False
    for shape in shapes:
        if cmds.getAttr( shape + '.io' ): continue
        if cmds.nodeType( shape ) == 'mesh':
            meshExists = True
            break
    if not meshExists: continue
    meshs.append( child )

if meshs:
    sgcommands.createSquashBend( meshs )