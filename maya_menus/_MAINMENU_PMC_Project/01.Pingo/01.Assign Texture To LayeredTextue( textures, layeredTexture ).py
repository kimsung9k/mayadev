from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

exs = sels[:-1]
target = sels[-1]

for ex in exs:
    sgCmds.assignToLayeredTexture( ex, target, blendMode=0 )