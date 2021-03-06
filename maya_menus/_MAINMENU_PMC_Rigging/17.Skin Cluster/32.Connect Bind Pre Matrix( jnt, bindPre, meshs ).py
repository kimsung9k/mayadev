from sgMaya import sgCmds
import maya.cmds as cmds
sels = cmds.ls( sl=1 )

jnt = sels[0]
bindPre = sels[1]
meshs = sels[2:]

for mesh in meshs:
    sgCmds.connectBindPreMatrix( jnt, bindPre, mesh )
cmds.select( jnt )