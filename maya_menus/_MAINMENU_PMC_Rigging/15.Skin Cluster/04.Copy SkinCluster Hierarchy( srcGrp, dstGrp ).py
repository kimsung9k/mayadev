import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
src = sels[0]
dst = sels[1]

srcChildren = pymel.core.listRelatives( src, c=1, ad=1, type='transform' )
dstChildren = pymel.core.listRelatives( dst, c=1, ad=1, type='transform' )

for i in range( len( srcChildren ) ):
    srcChild = srcChildren[i]
    dstChild = dstChildren[i]
    if not srcChild.getShape(): continue
    if not sgCmds.getNodeFromHistory( srcChild, 'skinCluster' ): continue
    sgCmds.autoCopyWeight( srcChild, dstChild )