from sgMaya import sgCmds
import maya.cmds as cmds
sels = cmds.ls( sl=1 )
sgCmds.copyWeightToSmoothedMesh( sels[0], sels[1] )