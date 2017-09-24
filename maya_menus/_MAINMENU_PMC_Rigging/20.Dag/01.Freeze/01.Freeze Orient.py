from sgMaya import sgCmds
sels = cmds.ls( sl=1 )
for sel in sels:
    sgCmds.freezeJoint( sel )