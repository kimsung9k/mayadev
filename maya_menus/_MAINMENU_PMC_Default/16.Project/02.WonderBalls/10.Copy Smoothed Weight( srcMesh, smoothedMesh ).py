from sgMaya import sgCmds
sels = cmds.ls( sl=1 )
sgCmds.copyWeightToSmoothedMesh( sels[0], sels[1] )