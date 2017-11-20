from sgMaya import sgCmds
from maya import cmds

sels = cmds.ls( sl=1, fl=1 )

for sel in sels:
    sgCmds.createFollicleOnSurface( sel )