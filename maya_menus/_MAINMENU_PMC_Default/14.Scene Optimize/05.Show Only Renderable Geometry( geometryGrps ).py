from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
selChildren = pymel.core.listRelatives( c=1, ad=1, type='transform' )

def isVisible( target ):
    if not target.v.get() and not target.v.listConnections(s=1, d=0): return False
    targetParents = target.getAllParents()
    for p in targetParents:
        if not p.v.get() and not p.v.listConnections(s=1, d=0): return False
    return True

visibleChildren = []
for child in selChildren:
    if child.nodeType() == 'place3dTexture':
        visibleChildren.append( child )
    childShape = child.getShape()
    if not childShape:
        continue
    cons = child.v.listConnections( s=1, d=0, type='animCurve' )
    if not childShape.nodeType() in ['mesh','FurFeedback']:
        if cons: pymel.core.delete( cons )
        continue
    if isVisible( child ):
        visibleChildren.append( child )

for child in selChildren:
    try:child.v.set( 0 )
    except:pass
    childShapes = child.listRelatives( s=1 )
    for childShape in childShapes:
        if childShape.nodeType() == 'nurbsCurve':
            try: childShape.v.set( 0 )
            except:pass

pymel.core.select( visibleChildren )
pymel.core.showHidden( a=1 )
pymel.core.select( sels )

for selChild in selChildren:
    vCons = selChild.v.listConnections( s=1, d=0, p=1 )
    if not vCons: continue
    try:selChild.v.set( vCons[0].get() )
    except:pass