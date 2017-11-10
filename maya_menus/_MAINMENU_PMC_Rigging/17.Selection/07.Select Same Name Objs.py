import maya.cmds as cmds

allNodes = cmds.ls()

sameNameObjs = []
for node in allNodes:
    if node.find( '|' ) != -1:
        print node
        sameNameObjs.append( node )

cmds.select( sameNameObjs )