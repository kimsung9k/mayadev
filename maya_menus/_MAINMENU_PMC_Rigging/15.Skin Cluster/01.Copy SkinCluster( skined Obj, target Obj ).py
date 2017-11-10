from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

srcMesh = sels[0]
others = sels[1:]

for other in others:
    children = other.listRelatives( c=1, ad=1, type='transform' )
    children.append( other )
    trs = []
    for child in children:
        shape = child.getShape()
        if not shape: continue
        trs.append( child )
    for tr in trs:
        sgCmds.autoCopyWeight( srcMesh, tr )