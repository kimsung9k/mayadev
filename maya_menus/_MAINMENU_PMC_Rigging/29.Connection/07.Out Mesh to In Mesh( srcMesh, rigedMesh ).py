import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

firstChildren = [ target for target in sels[0].listRelatives( c=1, ad=1, type='transform' ) if target.getShape() and target.getShape().nodeType() == 'mesh' ]
if not firstChildren: firstChildren = []
firstChildren.append( sels[0] )

secondChildren = [ target for target in sels[1].listRelatives( c=1, ad=1, type='transform' ) if target.getShape() and target.getShape().nodeType() == 'mesh' ]
if not secondChildren: secondChildren = []
secondChildren.append( sels[1] )

for i in range( len( firstChildren ) ):
    if not firstChildren[i].getShape(): continue
    sgCmds.outMeshToInMesh( firstChildren[i], secondChildren[i] )