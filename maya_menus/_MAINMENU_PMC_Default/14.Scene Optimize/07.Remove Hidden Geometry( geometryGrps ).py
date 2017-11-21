from sgMaya import sgCmds
from maya import mel
import pymel.core
sels = pymel.core.ls( sl=1 )
mel.eval( "DeleteHistory" )
selChildren = pymel.core.listRelatives( c=1, ad=1, type='transform' )

def isVisible( target ):
    if not target.v.get() and not target.v.listConnections(s=1, d=0): return False
    targetParents = target.getAllParents()
    for p in targetParents:
        if not p.v.get() and not p.v.listConnections(s=1, d=0): return False
    return True

hiddenTransforms = []
for child in selChildren:
    if isVisible( child ): continue
    hiddenTransforms.append( child )

pymel.core.delete( hiddenTransforms )