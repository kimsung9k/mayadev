from sgModules import sgcommands

sels = cmds.ls( sl=1 )

targets = []
for sel in sels:
    cmds.select( sel )
    putTarget =  cmds.joint()
    
    selName = sel.split('|')[-1]
    childName = ''
    if selName[-1] == '_':
        childName = sel.split('|')[-1] + 'child'
    else:
        childName = sel.split('|')[-1] + '_child'
        
    putTarget = cmds.rename( putTarget, childName )
    targets.append( putTarget )

cmds.select( targets )