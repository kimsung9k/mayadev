import maya.cmds as cmds
from sgModules import sgcommands
sels = cmds.ls( sl=1 )
sgcommands.setGeometryMatrixToTarget( sels[0], sels[1] )