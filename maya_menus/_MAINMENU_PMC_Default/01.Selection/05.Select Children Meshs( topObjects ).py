import maya.cmds as cmds

sels = cmds.ls( sl=1 )
selChildren = cmds.listRelatives( sels, c=1, ad=1, type='mesh', f=1 )

children = []
for child in selChildren:
    childP = cmds.listRelatives( child, p=1, f=1 )[0]
    children.append( childP )

cmds.select( children, add=1 )