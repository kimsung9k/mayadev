import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )
ctls = sels[:-1]
fbxRig = sels[-1]
ns = ''
if fbxRig.find( ':' ) != -1:
    ns = ':'.join( fbxRig.split( ':' )[:-1] )
fbxAttName = ns + ':FBXATT'

for ctl in ctls:
    if not pymel.core.objExists( fbxAttName ):
        fbxAtt = pymel.core.createNode( 'transform', n=fbxAttName )    
        fbxAtt.setParent( ns + ':FBXRIG' )
    keyAttrs = fbxAtt.listAttr( k=1 )
    for attr in keyAttrs:
        attr.setKeyable( False )
    else:
        fbxAtt = pymel.core.ls( fbxAttName )[0]
    
    attrs = ctl.listAttr( ud=1, k=1 )
    sgCmds.addOptionAttribute( fbxAtt, ctl.name().replace( 'FacialTitle', 'FacialCtl' ) )
    for attr in attrs:
        if attr.isLocked(): continue
        attrInfo = sgCmds.getAttrInfo( attr )
        sgCmds.createAttrByAttrInfo( attrInfo, fbxAtt )
        attr >> fbxAtt.attr( attr.attrName() )