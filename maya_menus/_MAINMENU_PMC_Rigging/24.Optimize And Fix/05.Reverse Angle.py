from sgMaya import sgCmds
import pymel.core

for sel in pymel.core.ls( sl=1 ):
    sgCmds.setAngleReverse( sel )