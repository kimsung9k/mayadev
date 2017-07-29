import maya.cmds as cmds

def getChildrenShapeExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        if cmds.nodeType( sel ) == 'transform':
            trNodes.append( sel )
        else:
            trNodes.append( cmds.listRelatives( sel, p=1, f=1 )[0] )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = cmds.listRelatives( sel, s=1, f=1 )[0]
        if not selShape: continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets


def addAttr( target, **options ):
    
    items = options.items()
    
    attrName = ''
    channelBox = False
    keyable = False
    for key, value in items:
        if key in ['ln', 'longName']:
            attrName = value
        elif key in ['cb', 'channelBox']:
            channelBox = True
            options.pop( key )
        elif key in ['k', 'keyable']:
            keyable = True 
            options.pop( key )
    
    if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
    
    cmds.addAttr( target, **options )
    
    if channelBox:
        cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        cmds.setAttr( target+'.'+attrName, e=1, k=1 )



def addModification( meshObjs ):
    
    meshObjs = getChildrenShapeExists( meshObjs )
    softMod = cmds.deformer( meshObjs, type='softMod' )[0]
    
    ctlGrp = cmds.createNode( 'transform' )
    cmds.setAttr( ctlGrp+'.dh', 1 )
    dcmp   = cmds.createNode( 'decomposeMatrix' )
    ctl = cmds.sphere()[0]
    ctl = cmds.parent( ctl, ctlGrp )[0]
    addAttr( ctl, ln='__________', at='enum', enumName = ':Modify Attr', cb=1 )
    addAttr( ctl, ln='falloffRadius', min=0, dv=1, k=1 )
    addAttr( ctl, ln='envelope', min=0, max=1, dv=1, k=1 )
    
    cmds.connectAttr( ctlGrp+'.wim', softMod+'.bindPreMatrix' )
    cmds.connectAttr( ctlGrp+'.wm', softMod+'.preMatrix' )
    cmds.connectAttr( ctl+'.wm', softMod+'.matrix' )
    cmds.connectAttr( ctl+'.m',  softMod+'.weightedMatrix' )
    
    cmds.connectAttr( ctlGrp+'.wm', dcmp+'.imat' )
    
    cmds.connectAttr( dcmp+'.ot', softMod+'.falloffCenter' )
    
    for i in range( len( meshObjs ) ):
        cmds.connectAttr( meshObjs[i]+'.wm', softMod+'.geomMatrix[%d]' % i )
    
    cmds.connectAttr( ctl+'.envelope', softMod+'.envelope' )
    cmds.connectAttr( ctl+'.falloffRadius', softMod+'.falloffRadius' )
    
    cmds.xform( ctlGrp, ws=1, t=cmds.getAttr( meshObjs[0]+'.wm' )[-4:-1] )
    cmds.select( ctlGrp )

addModification( cmds.ls( sl=1 ) )