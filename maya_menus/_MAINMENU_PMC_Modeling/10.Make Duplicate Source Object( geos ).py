from sgMaya import sgCmds
for sel in cmds.ls( sl=1, type='transform' ):
    sgCmds.DuplicateSourceObjectSet.makeDuplicateSourceObject( sel )