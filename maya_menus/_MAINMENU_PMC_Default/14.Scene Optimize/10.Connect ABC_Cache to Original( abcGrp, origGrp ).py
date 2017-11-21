from maya import cmds
import pymel.core
sels = pymel.core.ls( sl=1 )
src = sels[0]
trg = sels[1]

srcChildren = src.listRelatives( c=1, ad=1, type='transform' )
trgChildren = trg.listRelatives( c=1, ad=1, type='transform' )

for i in range( len( srcChildren ) ):
    srcChild = srcChildren[i]
    trgChild = trgChildren[i]
    
    keyAttrs = cmds.listAttr( srcChild.name(), k=1 )
    
    for keyAttr in keyAttrs:
        try:srcChild.attr( keyAttr ) >> trgChild.attr( keyAttr )
        except:pass

blendShapeNode = pymel.core.blendShape( src, trg )
blendShapeNode[0].w[0].set( 1 )