import maya.cmds as cmds

sels = cmds.ls( sl=1 )

for i in range( len( sels )-1 ):
   cmds.parent( sels[i], sels[i+1] )