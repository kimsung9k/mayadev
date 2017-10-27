from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
middleJnts = []
for sel in sels:
    middleJnt = sgCmds.addMiddleTranslateJoint( sel )
    middleJnts.append( middleJnt )
pymel.core.select( middleJnts )