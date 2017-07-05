import pymel.core
from sgMaya import sgCmds
ctls = pymel.core.ls( sl=1 )
fbxAttName = 'FBXATT'

if not pymel.core.objExists( fbxAttName ):
    fbxAtt = pymel.core.createNode( 'transform', n=fbxAttName )    
    fbxAtt.setParent( 'FBXRIG' )
    keyAttrs = fbxAtt.listAttr( k=1 )
    for attr in keyAttrs:
        attr.setKeyable( False )
else:
    fbxAtt = pymel.core.ls( fbxAttName )[0]

for ctl in ctls:
    attrs = ctl.listAttr( ud=1, k=1 )
    sgCmds.addOptionAttribute( fbxAtt, ctl.name().replace( 'FacialTitle', 'FacialCtl' ) )
    for attr in attrs:
        if attr.isLocked(): continue
        attrInfo = sgCmds.getAttrInfo( attr )
        sgCmds.createAttrByAttrInfo( attrInfo, fbxAtt )
        attr >> fbxAtt.attr( attr.attrName() )