import maya.cmds as cmds

sels = cmds.ls( sl=1 )
allFollicles = []
for sel in sels:
    follicles = cmds.listRelatives( sel, c=1, ad=1, f=1, type='follicle' )
    follicles.reverse()
    if cmds.nodeType( follicles ) == 'follicle':
        follicles.append( sel )
    allFollicles += follicles
cmds.select( allFollicles )