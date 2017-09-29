import maya.cmds as cmds
sels = cmds.ls( '*.transMult' )
targets = []
for sel in sels:
    target = sel.split( '.' )[0]
    if cmds.nodeType( target ) == 'joint':
        targets.append( target )
cmds.select( targets )