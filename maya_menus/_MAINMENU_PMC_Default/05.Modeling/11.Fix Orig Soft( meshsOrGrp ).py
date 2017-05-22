import maya.cmds as cmds

sels = cmds.listRelatives( cmds.ls( sl=1 ), c=1, ad=1, type='transform' )
if not sels:
    sels = cmds.ls( sl=1 )

targetOrigs= []
for sel in sels:
    shapes = cmds.listRelatives( sel, s=1, f=1 )
    if not shapes: continue
    for shape in shapes:
        if cmds.nodeType( shape ) != 'mesh': continue
        if cmds.listConnections( shape + '.inMesh', s=1, d=0 ): continue
        targetOrigs.append( shape )

for targetOrig in targetOrigs:
    cmds.polyNormalPerVertex( targetOrig, ufn=True )
    cmds.polySoftEdge( targetOrig, a=180, ch=0 )