import maya.cmds as cmds

sels = cmds.ls( sl=1 )

source = sels[0]
targets = sels[1:]

hists = cmds.listHistory( source, pdo=1 )
hists.reverse()

for hist in hists:
    print hist, cmds.nodeType( hist )
    if cmds.nodeType( hist ) == 'nonLinear':
        for target in targets:
            cmds.nonLinear( hist, e=1, geometry=target )
    elif cmds.nodeType( hist ) == 'wire':
        for target in targets:
            cmds.wire( hist, e=1, geometry=target )
    elif cmds.nodeType( hist ) == 'ffd':
        for target in targets:
            cmds.lattice( hist, e=1, geometry=target )