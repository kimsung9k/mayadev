import maya.cmds as cmds

for sel in cmds.ls( sl=1 ):
    refNode = cmds.referenceQuery( sel, rfn=1 )
    cmds.file( unloadReference = refNode )