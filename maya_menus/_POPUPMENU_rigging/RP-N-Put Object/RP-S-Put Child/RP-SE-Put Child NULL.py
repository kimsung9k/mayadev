from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

for sel in sels:
    putTarget = sgcommands.convertSg( sgcommands.putObject( sel, 'transform' ) )
    putTarget.attr( 'dh' ).set( 1 )
    sgcommands.parent( putTarget, sel )
    
    selName = sel.split('|')[-1]
    childName = ''
    if selName[-1] == '_':
        childName = sel.split('|')[-1] + 'child'
    else:
        childName = sel.split('|')[-1] + '_child'
    putTarget.rename( childName )