import maya.cmds as cmds
import meshFunctions
import skinClusterFunctions

putTypeList = ['joint', 'transform']
putType = putTypeList[0]


def getObjsCenter( objList ):

    minX = 100000000
    minY = 100000000
    minZ = 100000000
    maxX = -minX
    maxY = -minY
    maxZ = -minZ
    
    for obj in objList:
        if cmds.nodeType( obj ) == 'transform':
            objPos = cmds.xform( obj, q=1, ws=1, piv=1 )[:3]
        else:
            objPos = cmds.xform( obj, q=1, ws=1, t=1 )
        
        if minX >= objPos[0]:
            minX = objPos[0]
        if maxX < objPos[0]:
            maxX = objPos[0]
        
        if minY >= objPos[1]:
            minY = objPos[1]
        if maxY < objPos[1]:
            maxY = objPos[1]
        
        if minZ >= objPos[2]:
            minZ = objPos[2]
        if maxZ < objPos[2]:
            maxZ = objPos[2]
    
    centerX = (maxX + minX) * 0.5
    centerY = (maxY + minY) * 0.5
    centerZ = (maxZ + minZ) * 0.5
    
    return centerX, centerY, centerZ
    
    
def uiCmd_putToCenter( *args ):
    
    sels = cmds.ls( sl=1, fl=1 )
    
    centerPoint = getObjsCenter( sels )
    node = cmds.createNode( putType )
    
    cmds.setAttr( node+'.t', *centerPoint )



def uiCmd_putToVtxCenter( *args ):
    
    sels = cmds.ls( sl=1, fl=1 )
    
    points = cmds.ls( cmds.polyListComponentConversion( sels, tv=1 ), fl=1 )
    centerPoint = getObjsCenter( points )
    node = cmds.createNode( putType )
    
    cmds.setAttr( node+'.t', *centerPoint ) 
    
    
    
'''
def putAndBinding():
    
    sels = cmds.ls( sl=1, fl=1 )
    
    centerPoint = getObjsCenter( sels )
    jnt = cmds.createNode( 'joint' )
    
    cmds.setAttr( jnt+'.t', *centerPoint )
    
    meshObj = ''
    vtxIndex = None
    for sel in sels:
        selP = cmds.listRelatives( sel, p=1 )
        if not selP: continue
        if cmds.nodeType( selP[0] ) == 'mesh':
            meshObj = selP[0]
            vtxIndex = int( sel.split( '[' )[-1].replace( ']', '' ) )
            break
    
    if not meshObj: return None
    
    meshInfoInst = meshFunctions.MeshInfo( meshObj )
    vtxNames = meshInfoInst.getExpendLoof( vtxIndex )
    vtxIndices = meshInfoInst.expendedVertices
    
    skinCluster = ''
    hists = cmds.listHistory( meshObj )
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinCluster = hist
            break
    
    if not skinCluster:
        skinCluster = cmds.deformer( meshObj, type='skinCluster' )[0]
    
    skinClusterFunctions.appendInfluence(skinCluster, jnt, vtxIndices )
    
    cmds.select( vtxNames )'''