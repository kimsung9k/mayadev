from sgMaya import sgCmds
import maya.cmds as cmds

sels = cmds.ls( sl=1 )

first = sels[0]
others = sels[1:]

for other in others:
    sgCmds.copyShader( first, other )