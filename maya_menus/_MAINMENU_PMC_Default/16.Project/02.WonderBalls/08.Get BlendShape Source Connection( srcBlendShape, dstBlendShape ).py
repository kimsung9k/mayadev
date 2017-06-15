import pymel.core

sels = pymel.core.ls( sl=1 )

srcBlends = sels[:-1]
targetBlend = sels[-1]

targetBlendAttrs = targetBlend.weight

for srcBlend in srcBlends:
    for i in range( srcBlend.weight.numElements() ):
        attrName = cmds.ls( srcBlend.weight[i].name() )[0].split( '.' )[-1]
        
        cons = srcBlend.weight[i].listConnections( s=1, p=1 )
        
        if pymel.core.attributeQuery( attrName , node=targetBlend, ex=1 ):
            cons[0] >> targetBlend.attr( attrName )