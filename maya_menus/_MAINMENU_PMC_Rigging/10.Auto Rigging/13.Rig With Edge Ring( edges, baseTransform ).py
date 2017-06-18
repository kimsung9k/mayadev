from sgMaya import sgCmds
sels = cmds.ls( sl=1, fl=1 )
sgCmds.rigWithEdgeRing( sels[:-1], sels[-1] )