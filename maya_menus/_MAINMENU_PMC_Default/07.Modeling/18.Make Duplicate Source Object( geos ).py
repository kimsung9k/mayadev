from sgModules import sgMessageCommands
for sel in cmds.ls( sl=1, type='transform' ):
    sgMessageCommands.DuplicateSourceObjectSet.makeDuplicateSourceObject( sel )