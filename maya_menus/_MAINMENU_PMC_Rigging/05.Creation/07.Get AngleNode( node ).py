from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    if sel.nodeType() in ['transform', 'joint']:
        outputAttr = sel.t
    elif sel.nodeType() == 'decomposeMatrix':
        outputAttr = sel.ot
    else:
        outputAttr = sel.output
    
    angleNodes.append( sgCmds.getAngleNode( outputAttr ) )

pymel.core.select( angleNodes )