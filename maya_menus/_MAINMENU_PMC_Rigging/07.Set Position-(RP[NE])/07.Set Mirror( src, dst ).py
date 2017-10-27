from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
src = sels[0]
dst = sels[1]
sgCmds.setMirrorTransform( src, dst )