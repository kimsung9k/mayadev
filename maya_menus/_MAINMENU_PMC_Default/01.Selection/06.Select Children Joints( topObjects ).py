import maya.cmds as cmds

sels = cmds.ls( sl=1 )
allJnts = []
for sel in sels:
    jnts = cmds.listRelatives( sel, c=1, ad=1, f=1, type='joint' )
    jnts.reverse()
    if cmds.nodeType( sel ) == 'joint':
        jnts.append( sel )
    allJnts += jnts
cmds.select( allJnts, tgl=1 )