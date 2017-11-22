from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
children = pymel.core.listRelatives( sels, c=1, ad=1, f=1, type='transform' )
if not children: children = []
children += sels

meshs = []
for child in children:
    shapes = child.listRelatives( s=1, f=1 )
    if not shapes: continue
    meshExists = False
    for shape in shapes:
        if shape.io.get(): continue
        if shape.nodeType() == 'mesh':
            meshExists = True
            break
    if not meshExists: continue
    meshs.append( child )

if meshs:
    sgCmds.createSquashBend( meshs )