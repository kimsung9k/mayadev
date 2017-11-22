from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
mtxNode = sgCmds.getFbfMatrix( sels[0], sels[1], sels[2] )
pymel.core.select( mtxNode )