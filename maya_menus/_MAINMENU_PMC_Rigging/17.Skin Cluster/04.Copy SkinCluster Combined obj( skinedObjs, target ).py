from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

bindJoints = []

for sel in sels:
    skinNodes = sgCmds.getNodeFromHistory( sel, 'skinCluster' )
    
    if not skinNodes: continue
    joints = cmds.listConnections( skinNodes[0] + '.matrix' )
    
    bindJoints += joints
    
cmds.skinCluster( bindJoints, sels[-1], tsb=1 )
cmds.select( sels )
cmds.copySkinWeights( noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )