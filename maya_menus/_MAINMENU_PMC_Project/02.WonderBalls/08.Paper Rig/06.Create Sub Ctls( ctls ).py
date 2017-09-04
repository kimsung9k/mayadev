from sgMaya import sgCmds
import maya.cmds as cmds
sels = cmds.ls( sl=1 )
for sel in sels:
    sgCmds.makeSubCtl( sel )