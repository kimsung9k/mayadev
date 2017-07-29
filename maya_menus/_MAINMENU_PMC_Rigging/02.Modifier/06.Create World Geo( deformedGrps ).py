from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
children = pymel.core.listRelatives( sels, c=1, ad=1, type='transform' )
if not children: children = []
children += sels
for child in children:
    if not child.getShape(): continue
    nodeType = child.getShape().nodeType()
    if not nodeType in ['mesh', 'nurbsCurve']: continue
    pWorldGeo = sgCmds.makeCloneObject( child.getParent(), cloneAttrName='worldGeo' )
    worldGeo = sgCmds.getWorldGeometry( child ).getParent()
    worldGeo.setParent( pWorldGeo )
    worldGeo.rename( child )