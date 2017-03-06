import maya.cmds as cmds


def getIndicesFromSelected():
    
    sels = cmds.ls( cmds.polyListComponentConversion( cmds.ls( sl=1 ), toVertex = 1 ), fl=1 )

    strIndices = ''
    targetMesh = ''
    for sel in sels:
        mesh, vtx = sel.split( '.' )
        strIndex = sel.split( '[' )[-1].replace( ']', '' )
        strIndices += strIndex + ","

        if cmds.nodeType( mesh ) == 'transform':
            shapes = cmds.listRelatives( mesh, s=1 )
            if not shapes:return None
            mesh = shapes[0]
        
        if not targetMesh:
            targetMesh = mesh
        else:
            if mesh != targetMesh:
                return None
    
    return targetMesh, strIndices[:-1]



def getMeshFromSelected():
    
    sels = cmds.ls( sl=1 )
    
    target = sels[-1]
    
    if cmds.nodeType( target ) == 'mesh':
        return target
    elif cmds.nodeType( target ) == 'transform':
        shapes = cmds.listRelatives( target, s=1 )
        if not shapes: return None
        if cmds.nodeType( shapes[0] ) == 'mesh':
            return shapes[0]
        
        
        
def createRivet( meshName, centerIndices, aimPivIndices, aimIndices, upPivIndices, upIndices, aimIndex, upIndex ):
    
    rivetObject = cmds.group( em=1 )
    cmds.setAttr( rivetObject+'.dh', 1 )
    cmds.setAttr( rivetObject+'.dla', 1 ) 
    
    rivetNode = cmds.createNode( 'meshRivet' )
    cmds.setAttr( rivetNode+'.aimAxis', aimIndex )
    cmds.setAttr( rivetNode+'.upAxis',  upIndex  )
    
    for i in range( len( centerIndices ) ):
        cmds.setAttr( rivetNode+'.centerIndices[%d]' % i, centerIndices[i] )
    for i in range( len( aimPivIndices ) ):
        cmds.setAttr( rivetNode+'.aimPivIndices[%d]' % i, aimPivIndices[i] )
    for i in range( len( aimIndices ) ):
        cmds.setAttr( rivetNode+'.aimIndices[%d]' % i, aimIndices[i] )
    for i in range( len( upPivIndices ) ):
        cmds.setAttr( rivetNode+'.upPivIndices[%d]' % i, upPivIndices[i] )
    for i in range( len( upIndices ) ):
        cmds.setAttr( rivetNode+'.upIndices[%d]' % i, upIndices[i] )
    
    cmds.connectAttr( meshName+'.outMesh', rivetNode+'.inputMesh' )
    cmds.connectAttr( meshName+'.wm', rivetNode+'.meshMatrix' )
    cmds.connectAttr( rivetObject+'.pim', rivetNode+'.parentInverseMatrix' )
    cmds.connectAttr( rivetNode+'.ot', rivetObject+'.t' )
    cmds.connectAttr( rivetNode+'.or', rivetObject+'.r' )
    
    return rivetObject