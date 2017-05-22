import maya.cmds as cmds

sels = cmds.ls( type='joint' )

jnts = []

for sel in sels:
    colorIndex = cmds.getAttr( sel + '.overrideColor' )
    if colorIndex == 14:
        jnts.append( sel )

cmds.select( jnts )