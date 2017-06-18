from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

jnts = sels[:-1]
mesh = sels[-1]
for jnt in jnts:
    sgCmds.addInfluenceOnlyOneCloseVertex( jnt, mesh )