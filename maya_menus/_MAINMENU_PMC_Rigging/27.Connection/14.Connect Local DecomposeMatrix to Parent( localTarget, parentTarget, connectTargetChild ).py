from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
localTarget = sels[0]
parentTarget = sels[1]
connectTarget = sels[2].getParent()
dcmp = sgCmds.getLocalDecomposeMatrix( localTarget.wm, parentTarget.wim )
dcmp.ot >> connectTarget.t
dcmp.outputRotate >> connectTarget.r