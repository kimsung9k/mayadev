from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
for sel in sels:
    selP = sel.getParent()
    if not selP: continue
    selP.rename( 'P' + sel.nodeName() )