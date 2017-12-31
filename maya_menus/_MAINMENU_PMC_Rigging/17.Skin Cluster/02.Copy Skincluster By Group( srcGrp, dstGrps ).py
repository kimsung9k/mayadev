from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

srcMesh = sels[0]
others = sels[1:]

srcChildren = srcMesh.listRelatives( c=1, ad=1, type='transform' )

for other in others:
    children = other.listRelatives( c=1, ad=1, type='transform' )
    
    for i in range( len( srcChildren ) ):
        if not sgCmds.getNodeFromHistory( srcChildren[i], 'skinCluster' ): continue
        sgCmds.autoCopyWeight( srcChildren[i], children[i] )