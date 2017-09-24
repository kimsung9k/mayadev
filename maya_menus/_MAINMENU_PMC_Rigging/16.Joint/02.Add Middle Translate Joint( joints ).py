from sgModules import sgcommands
import maya.cmds as cmds

sels =cmds.ls( sl=1 )
middleJnts = []
for sel in sels:
    middleJnt = sgcommands.addMiddleTranslateJoint( sel )
    middleJnts.append( middleJnt )

cmds.select( middleJnts )