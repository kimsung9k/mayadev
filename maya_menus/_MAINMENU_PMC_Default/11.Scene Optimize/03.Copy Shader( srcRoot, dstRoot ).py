import pymel.core

sels = pymel.core.ls( sl=1 )

srcRoot = sels[0]
dstRoot = sels[1]

srcNs = ':'.join( srcRoot.split( ':' )[:-1] )
dstNs = ':'.join( dstRoot.split( ':' )[:-1] )

srcChildren = srcRoot.listRelatives( c=1, ad=1, type='transform' )
srcChildren.append( srcRoot )

for srcChild in srcChildren:
    srcShape = srcChild.getShape()
    if not srcShape: continue
    shadingEngine = srcShape.listConnections( s=0, d=1, type='shadingEngine' )
    if not shadingEngine: continue
    dstChild = srcChild.replace( srcNs, dstNs )
    if not cmds.objExists( dstChild ): continue
    cmds.sets( dstChild, e=1, forceElement = shadingEngine[0].name() )