from sgMaya import sgAnim
sels = cmds.ls( sl=1 )
for sel in sels:
    sgAnim.makeWaveJoint( sel )
cmds.select( sels )