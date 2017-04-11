import maya.cmds as cmds


def blendAndFix_toSkin( targetMeshObj ):

    hists = cmds.listHistory( targetMeshObj, pdo=1 )
    
    if not hists: return None
    
    skinClusterEx = False
    targetGroupParts = None
    
    for hist in hists:
        if cmds.nodeType( hist ) == 'blendAndFixedShape':
            return hist
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinClusterEx = True
            continue
            
        if skinClusterEx:
            if cmds.nodeType( hist ) == 'groupParts':
                if not targetGroupParts:
                    targetGroupParts = hist
                    continue
            if cmds.nodeType( hist ) == 'tweak':
                cmds.delete( hist )
                break
    
    if not targetGroupParts: return None
    
    inputGeoCon = cmds.listConnections( targetGroupParts+'.inputGeometry', p=1, c=1 )[1]
    inputGeo = inputGeoCon.split( '.' )[0]
    
    if cmds.nodeType( inputGeo ) != 'mesh':
        meshNode = cmds.createNode( 'mesh' )
        meshObj = cmds.listRelatives( meshNode, p=1 )[0]
        output = cmds.listConnections( targetGroupParts+'.inputGeometry', s=1, d=0, c=1, p=1 )[1]
        cmds.connectAttr( output, meshObj+'.inMesh' )
        cmds.connectAttr( meshNode+'.outMesh', targetGroupParts+'.inputGeometry', f=1 )
        cmds.parent( meshNode, targetMeshObj, add=1, shape=1 )
        cmds.delete( meshObj )
        inputGeo = meshNode
    
    
    if cmds.getAttr( inputGeo+'.io' ):
        cmds.setAttr( inputGeo+'.io', 0 )
    
    cmds.setAttr( inputGeo+'.io', 0 )
    cmds.deformer( inputGeo, type='blendAndFixedShape' )
    cmds.setAttr( inputGeo+'.io', 1 )
    
    if not cmds.getAttr( inputGeo+'.io' ):
        cmds.setAttr( inputGeo+'.io', 1 )
    
    hists = cmds.listHistory( targetMeshObj, pdo=1 )
    
    returnNode = None
    
    for hist in hists:
        if cmds.nodeType( hist ) == 'blendAndFixedShape':
            returnNode = hist
            continue
    
    cmds.delete( inputGeo )

    return returnNode


def blendAndFixedShapeExists( targetMeshObj ):
    
    hists = cmds.listHistory( targetMeshObj, pdo=1 )
    
    if not hists: return None
    
    skinClusterEx = False
    
    for hist in hists:
        if skinClusterEx:
            if cmds.nodeType( hist ) == 'blendAndFixedShape':
                return True
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinClusterEx = True
            continue
    
    return False