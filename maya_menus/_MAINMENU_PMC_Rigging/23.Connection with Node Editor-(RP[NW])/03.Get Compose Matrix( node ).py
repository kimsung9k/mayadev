from sgMaya import sgCmds
import pymel.core

composeList = [ sgCmds.getComposeMatrix_fromNode( sel ) for sel in pymel.core.ls( sl=1 ) ]
pymel.core.select( composeList )