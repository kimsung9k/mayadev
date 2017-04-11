import maya.cmds as cmds

sels = cmds.ls( sl=1 )

sameNameObjs = []
for sel in sels:
    if sel.find( '|' ) != -1:
        sameNameObjs.append( sel )

cmds.select( sameNameObjs )