targets = cmds.ls( sl=1 )

for target in targets:
    refCons = cmds.listConnections( target + '.refNode', s=1, d=0, p=1, c=1 )
    refNode = refCons[1].split( '.' )[0]
    cmds.disconnectAttr( refCons[1], refCons[0] )
    cmds.file( loadReference = refNode )    
    cmds.connectAttr( refCons[1], refCons[0] )
    cmds.setAttr( target + '.v', 0 )