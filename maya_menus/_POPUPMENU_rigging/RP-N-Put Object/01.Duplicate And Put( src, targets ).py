import maya.cmds as cmds
sels = cmds.ls( sl=1 )
ctl = sels[0]
others = sels[1:]

for other in others:
    duCtl = cmds.duplicate( ctl )[0]
    cmds.xform( duCtl, ws=1, matrix= cmds.getAttr( other + '.wm' ) )