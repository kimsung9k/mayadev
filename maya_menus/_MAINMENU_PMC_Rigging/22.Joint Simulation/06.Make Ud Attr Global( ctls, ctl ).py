from sgMaya import sgAnim
sels = cmds.ls( sl=1 )
targets = sels[:-1]
ctl = sels[-1]
sgAnim.makeUdAttrGlobal( targets, ctl )
cmds.select( ctl )