import maya.cmds as cmds

sels = cmds.ls( sl=1 )
sels[0] = cmds.rename( sels[0], 'Ctl_Move' )

selP = cmds.listRelatives( sels[0], f=1, p=1 )
if selP:
    cmds.rename( selP, 'P' + sels[0] )