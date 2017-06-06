from sgMaya import sgAnim
sels = cmds.ls( sl=1 )
topJoints = sels[:-1]
ctl = sels[-1]
sgAnim.makeWaveGlobal( topJoints, ctl )
cmds.select( topJoints )