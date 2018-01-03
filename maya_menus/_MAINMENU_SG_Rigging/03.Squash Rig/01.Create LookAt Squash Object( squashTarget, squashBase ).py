from sgMaya import sgCmds, sgRig
import pymel.core
sels = pymel.core.ls( sl=1 )
squashCenter = sgRig.makeLookAtSquashTransform( sels[0], sels[1] )