from sgModules import sgcommands
import maya.cmds as cmds

sgcommands.combineMultiShapes( cmds.ls( sl=1 ) )