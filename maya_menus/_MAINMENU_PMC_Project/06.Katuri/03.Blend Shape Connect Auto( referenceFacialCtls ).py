import pymel.core
sels = pymel.core.ls( sl=1 )

targetBlendShape = pymel.core.ls( 'blendShape1' )[0]

for sel in sels:
    selAttrs = sel.listAttr( k=1 )
    realCtl = pymel.core.ls( sel.split( ':' )[-1] )[0]
    for attr in selAttrs:
        dstCons = attr.listConnections( s=0, d=1, p=1 )
        realCtlAttr = realCtl.attr( attr.attrName() )
        for dstCon in dstCons:
            dstNode = dstCon.node()
            if dstNode.nodeType() == 'animCurveUU':
                if not dstNode.output.listConnections( p=1 ): continue
                blendAttrName = cmds.ls( dstNode.output.listConnections( p=1 )[0].name() )[0].split( '.' )[-1]
                duAnimCurve = pymel.core.duplicate( dstNode )[0]
                realCtlAttr >> duAnimCurve.input
                duAnimCurve.output >> targetBlendShape.attr( blendAttrName )
            else:
                blendAttrName = cmds.ls( dstCon.name() )[0].split( '.' )[-1]
                realCtlAttr >> targetBlendShape.attr( blendAttrName )