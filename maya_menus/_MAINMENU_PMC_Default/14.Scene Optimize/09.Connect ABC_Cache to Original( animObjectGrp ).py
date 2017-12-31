from sgMaya import sgCmds
from maya import mel
import pymel.core
animObjects = pymel.core.ls( sl=1 )
mel.eval( "DeleteHistory" )
selChildren = pymel.core.listRelatives( animObjects, c=1, ad=1, type='transform' )

def isVisible( target ):
    if not target.attr( 'v' ).get() and not target.attr( 'v' ).listConnections(s=1, d=0): return False
    targetParents = target.getAllParents()
    for p in targetParents:
        if not p.attr( 'v' ).get() and not p.v.listConnections(s=1, d=0): return False
    return True

hiddenTransforms = []
for child in selChildren:
    if isVisible( child ) or child.nodeType() == 'place3dTexture': continue
    hiddenTransforms.append( child )

pymel.core.delete( hiddenTransforms )

sels = pymel.core.ls( type='decomposeMatrix' )
sels += pymel.core.ls( type='multMatrix' )
pymel.core.delete( sels )

trgChildren = animObjects[0].listRelatives( c=1, ad=1, type='transform' )

for i in range( len( trgChildren ) ):
    trgChild = trgChildren[i]
    srcChild = trgChild.longName().replace( ':', '_' ).replace( '|animObjects', '|abcs' )
    if not cmds.objExists( srcChild ):
        print "not exists : ", srcChild
        continue
    srcChild = pymel.core.ls( srcChild )[0]
    
    keyAttrs = cmds.listAttr( srcChild.name(), k=1 )
    
    for keyAttr in keyAttrs:
        try:srcChild.attr( keyAttr ) >> trgChild.attr( keyAttr )
        except:pass

    if srcChild.getShape() and srcChild.getShape().nodeType() == 'mesh':
        blendShapeNode = pymel.core.blendShape( srcChild, trgChild )
        blendShapeNode[0].w[0].set( 1 )