from sgMaya import sgCmds
import maya.cmds as cmds
sels = cmds.ls( sl=1 )

jnts = sels[:-1]
mesh = sels[-1]
for jnt in jnts:
    sgCmds.addInfluenceOnlyOneCloseVertex( jnt, mesh )