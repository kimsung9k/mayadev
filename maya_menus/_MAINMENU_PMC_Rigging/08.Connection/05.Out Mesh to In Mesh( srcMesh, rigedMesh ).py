import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

firstChildren = sels[0].listRelatives( c=1, ad=1, type='transform' )
if not firstChildren: firstChildren = []
firstChildren.append( sels[0] )

secondChildren = sels[1].listRelatives( c=1, ad=1, type='transform' )
if not secondChildren: secondChildren = []
secondChildren.append( sels[1] )
print len( firstChildren )
for i in range( len( firstChildren ) ):
    if not firstChildren[i].getShape(): continue
    sgCmds.outMeshToInMesh( firstChildren[i], secondChildren[i] )