from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

src = sels[0]
trg = sels[1]

attrs = src.getShape().listAttr( ud=1 )
for attr in attrs:
    attrName = attr.longName()
    if attrName.find( 'shape_t' ) != -1:
        trg.attr( attrName ).set( -attr.get() )
    else:
        trg.attr( attrName ).set( attr.get() )