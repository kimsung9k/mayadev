import maya.cmds as cmds

sels = cmds.ls( sl=1 )

for i in range( len( sels )-1 ):
    selP = cmds.listRelatives( sels[i], p=1, f=1 )
    if selP:
        cmds.parent( selP[0], sels[i+1] )
    else:
        cmds.parent( sels[i], sels[i+1] )