import maya.cmds as cmds
from sgMaya import sgCmds
sels = cmds.ls( sl=1 )
ctl = sels[0]
others = sels[1:]

duObjs = [ctl]
for other in others:
    duCtl = cmds.duplicate( ctl )[0]
    sgCmds.setMatrixToTarget( sgCmds.getPivotWorldMatrix( other ), duCtl )
    cmds.delete( other )
    duObjs.append( duCtl )
pymel.core.select( duObjs )