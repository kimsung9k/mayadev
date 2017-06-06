from sgModules import sgcommands

sels = cmds.ls( sl=1 )

exs = sels[:-1]
target = sels[-1]

for ex in exs:
    sgcommands.assignToLayeredTexture( ex, target, blendMode=0 )