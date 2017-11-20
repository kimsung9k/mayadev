from sgMaya import sgCmds
from maya import cmds

for sel in cmds.ls( sl=1 ):
    sgCmds.freezeByParent( sel )