from sgModules import sgcommands
import maya.cmds as cmds
sgcommands.createRigedCurve( cmds.ls( sl=1 ) )