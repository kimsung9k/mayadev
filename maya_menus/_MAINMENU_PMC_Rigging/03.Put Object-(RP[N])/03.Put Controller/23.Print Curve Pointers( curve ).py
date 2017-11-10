from sgMaya import sgCmds
import pymel.core
sgCmds.printCurvePoints(  pymel.core.ls( sl=1 )[0] )