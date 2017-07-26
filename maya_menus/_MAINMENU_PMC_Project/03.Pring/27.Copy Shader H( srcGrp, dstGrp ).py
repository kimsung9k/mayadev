import pymel.core

sels = pymel.core.ls( sl=1 )

srcRoot = sels[0]
dstRoot = sels[1]

srcChildren = srcRoot.listRelatives( c=1, ad=1, type='transform' )
dstChildren = dstRoot.listRelatives( c=1, ad=1, type='transform' )

for i in range( len( srcChildren ) ):
    srcChild = srcChildren[i]
    srcShape = srcChild.getShape()
    if not srcShape: continue
    shadingEngine = srcShape.listConnections( s=0, d=1, type='shadingEngine' )
    if not shadingEngine: continue
    dstChild = dstChildren[i]
    if not pymel.core.objExists( dstChild ): continue
    cmds.sets( dstChild.name(), e=1, forceElement = shadingEngine[0].name() )