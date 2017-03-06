import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import format
from sgModules import sgbase



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
                vtxList = sgbase.getInt2Ptr()
                fnMesh.getEdgeVertices( elements[j], vtxList )
                values = sgbase.getListFromInt2Ptr(vtxList)
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





def getCenter( sels ):
    
    if not sels: return None
    
    bb = OpenMaya.MBoundingBox()
    
    selVerticesList = selectedVertices(sels)
    
    if selVerticesList:
        for selVertices in selVerticesList:
            dagPath, vtxIds = selVertices
            fnMesh = OpenMaya.MFnMesh( dagPath )
            points = OpenMaya.MPointArray()
            fnMesh.getPoints( points, OpenMaya.MSpace.kWorld )
            for i in range( vtxIds.length() ):
                bb.expand( points[vtxIds[i]] )
    else:
        for sel in sels:
            pos = OpenMaya.MPoint( *cmds.xform( sel, q=1, ws=1, t=1 ) )
            bb.expand( pos )
    
    return bb.center()



def getSelectionType( sel ):
    return sgbase.getMObject( sel ).apiTypeStr()

