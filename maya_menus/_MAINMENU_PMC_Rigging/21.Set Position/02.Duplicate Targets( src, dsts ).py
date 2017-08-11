import maya.cmds as cmds

sels = cmds.ls( sl=1 )

src = sels[0]
dsts = sels[1:]

for dst in dsts:
    duSrc = cmds.duplicate( src )[0]
    dstMtx = cmds.getAttr( dst + '.wm' )
    cmds.xform( duSrc, ws=1, matrix=dstMtx )