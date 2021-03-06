from sgMaya import sgCmds
import maya.cmds as cmds

sels = cmds.ls( sl=1 )
target = sels[-1]
targetMtxList = cmds.getAttr( target + '.wm' )

for sel in sels[:-1]:
    sgCmds.setMatrixToTarget( targetMtxList, sel )