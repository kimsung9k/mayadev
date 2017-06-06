from sgModules import sgcommands
for sel in cmds.ls( sl=1, type='transform' ):
    sgcommands.DuplicateSourceObjectSet.makeDuplicateSourceObject( sel )