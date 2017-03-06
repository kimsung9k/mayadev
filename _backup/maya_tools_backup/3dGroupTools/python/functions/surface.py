import maya.cmds as cmds


def getCloseSurfaceNode( target, surface ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    closeNode = cmds.createNode( 'closestPointOnSurface' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( target+'.wm', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.ot', closeNode+'.inPosition' )
    cmds.connectAttr( surfShape+'.worldSpace', closeNode+'.inputSurface' )
    
    return closeNode



def getPointOnSurfaceNode( target, surface, keepClose=False ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    node = cmds.createNode( 'pointOnSurfaceInfo' )
    cmds.connectAttr( surfShape+'.local', node+'.inputSurface' )
    
    closeNode = getCloseSurfaceNode( target, surface )
    
    if not keepClose:
        cmds.setAttr( node+'.u', cmds.getAttr( closeNode+'.u' ) )
        cmds.setAttr( node+'.v', cmds.getAttr( closeNode+'.v' ) )
        cmds.delete( closeNode )
    else:
        cmds.connectAttr( closeNode+'.u', node+'.u' )
        cmds.connectAttr( closeNode+'.v', node+'.v' )
    
    return node



def createTransformOnSurface( target, surface, keepClose=False ):
    
    pointOnSurfNode = getPointOnSurfaceNode( target, surface, keepClose )
    
    tr = cmds.createNode( 'transform', n='P'+target )
    fbfMtx = cmds.createNode( 'fourByFourMatrix' )
    dcmp   = cmds.createNode( 'decomposeMatrix' )
    vectorNode = cmds.createNode( 'vectorProduct' )
    cmds.setAttr( vectorNode+'.op', 2 )
    cmds.connectAttr( pointOnSurfNode+'.tu', vectorNode+'.input1' )
    cmds.connectAttr( pointOnSurfNode+'.n', vectorNode+'.input2' )
    cmds.connectAttr( vectorNode+'.outputX', fbfMtx+'.i00' )
    cmds.connectAttr( vectorNode+'.outputY', fbfMtx+'.i01' )
    cmds.connectAttr( vectorNode+'.outputZ', fbfMtx+'.i02' )
    cmds.connectAttr( pointOnSurfNode+'.px', fbfMtx+'.i30' )
    cmds.connectAttr( pointOnSurfNode+'.py', fbfMtx+'.i31' )
    cmds.connectAttr( pointOnSurfNode+'.pz', fbfMtx+'.i32' )
    cmds.connectAttr( pointOnSurfNode+'.nx', fbfMtx+'.i10' )
    cmds.connectAttr( pointOnSurfNode+'.ny', fbfMtx+'.i11' )
    cmds.connectAttr( pointOnSurfNode+'.nz', fbfMtx+'.i12' )
    cmds.connectAttr( pointOnSurfNode+'.position', tr+'.t' )
    cmds.connectAttr( fbfMtx+'.output', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.or', tr+'.r' )
    
    cmds.setAttr( tr+'.dh', 1 )
    cmds.setAttr( tr+'.dla', 1 )