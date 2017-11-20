import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import get


def getInt2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList([0,0],2)
    return util.asInt2Ptr()




def getListFromInt2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getInt2ArrayItem( ptr, 0, 0 )
    v2 = util.getInt2ArrayItem( ptr, 0, 1 )
    return [v1, v2]


def selectedVertices( targetObj=None ):
    
    cmds.select( targetObj )
    selList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selList)
    
    returnTargets = []
    for i in range( selList.length() ):
        dagPath    = OpenMaya.MDagPath()
        oComponent = OpenMaya.MObject()
        
        selList.getDagPath( i, dagPath, oComponent )
        
        if dagPath.node().apiTypeStr() != 'kMesh': continue 
        
        fnMesh = OpenMaya.MFnMesh( dagPath )
        targetVertices = OpenMaya.MIntArray()
        if oComponent.isNull(): continue
        
        singleComp = OpenMaya.MFnSingleIndexedComponent( oComponent )
        elements = OpenMaya.MIntArray()
        singleComp.getElements( elements )
            
        
        if singleComp.componentType() == OpenMaya.MFn.kMeshVertComponent :
            for j in range( elements.length() ):
                targetVertices.append( elements[j] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshEdgeComponent:
            for j in range( elements.length() ):
                vtxList = getInt2Ptr()
                fnMesh.getEdgeVertices( elements[j], vtxList )
                values = getListFromInt2Ptr(vtxList)
                targetVertices.append( values[0] )
                targetVertices.append( values[1] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshPolygonComponent:
            for j in range( elements.length() ):
                intArr = OpenMaya.MIntArray()
                fnMesh.getPolygonVertices( elements[j], intArr )
                for k in range( intArr.length() ):
                    targetVertices.append( intArr[k] )
        
        if targetVertices.length():
            returnTargets.append( [dagPath, targetVertices] )
    
    return returnTargets


def getIntPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asIntPtr()



def averageNormal( *args ):
    
    for dagPath, vtxList in selectedVertices():
        fnMesh = OpenMaya.MFnMesh( dagPath )
        
        points = OpenMaya.MPointArray()
        normals = OpenMaya.MFloatVectorArray()
        
        fnMesh.getPoints( points )
        fnMesh.getVertexNormals( True, normals )
        
        itMeshVtx = OpenMaya.MItMeshVertex( dagPath )
        
        resultPoints = []
        for i in range( vtxList.length() ):
            pPrevIndex = getIntPtr()
            itMeshVtx.setIndex( vtxList[i], pPrevIndex )
            conVertices = OpenMaya.MIntArray();
            itMeshVtx.getConnectedVertices(conVertices)
            
            bb = OpenMaya.MBoundingBox()
            for j in range( conVertices.length() ):
                bb.expand( points[conVertices[j]] )
            
            center = bb.center()
            centerVector = points[ vtxList[i] ] - center
            normal       = normals[ vtxList[i] ]
            normal.normalize()
            projVector = normal * ( normal * OpenMaya.MFloatVector(centerVector) )
            
            resultPoint = -OpenMaya.MVector(projVector)/3.0 + OpenMaya.MVector( points[ vtxList[i] ] )
            resultPoints.append( resultPoint )
        
        meshName = fnMesh.partialPathName()
        for i in range( vtxList.length() ):
            cmds.move( resultPoints[i].x, resultPoints[i].y, resultPoints[i].z, meshName + ".vtx[%d]" % vtxList[i], os=1 )




def createOutMesh( meshObject, *args ):
    
    nonIoMeshs = get.nonIoMesh( meshObject )
    if not nonIoMeshs: 
        cmds.error( "No meshs are selected" )
        return None
    
    srcMesh = nonIoMeshs[0]
    srcMeshTransform = cmds.listRelatives( srcMesh, p=1, f=1 )[0]
    
    newMesh = cmds.createNode( "mesh" )
    newMeshTransform = cmds.listRelatives( newMesh, p=1, f=1 )[0]
    
    cmds.connectAttr( srcMesh + ".outMesh", newMesh + ".inMesh" )
    cmds.xform( newMeshTransform, ws=1, matrix= cmds.getAttr( srcMeshTransform + ".wm" ) )

    newMeshTransform = cmds.rename( newMeshTransform, 'out_'+srcMeshTransform.split( '|' )[-1] )
    return newMeshTransform


def deleteHistory( target, evt=0 ):

    meshs = get.nonIoMesh( target )
    
    for mesh in meshs:
        srcPlug = cmds.listConnections( mesh + '.inMesh', s=1, d=0, p=1 )
        cmds.disconnectAttr( srcPlug[0], mesh + '.inMesh' )
        srcNode = srcPlug[0].split( '.' )[0]
        cmds.delete( srcNode )