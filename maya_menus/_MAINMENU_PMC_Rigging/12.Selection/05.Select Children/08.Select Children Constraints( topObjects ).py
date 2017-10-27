import maya.cmds as cmds

sels = cmds.ls( sl=1 )
allConstraints = []
for sel in sels:
    constrains = cmds.listRelatives( sel, c=1, ad=1, f=1, type='constraint' )
    if not constrains: constrains = []
    constrains.reverse()
    if cmds.nodeType( sel ).lower().find('constrain') != -1:
        constrains.append( sel )
    allConstraints += constrains
cmds.select( allConstraints )