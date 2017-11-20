import maya.OpenMaya as om
import maya.cmds as cmds
import math


def getMFnMesh( meshName ):
    selList = om.MSelectionList()
    selList.add( meshName )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return om.MFnMesh( dagPath )


def getUVs( mesh ):
    
    fnMesh = getMFnMesh( mesh )
    
    uArray = om.MFloatArray()
    vArray = om.MFloatArray()
    fnMesh.getUVs( uArray, vArray )
    
    print fnMesh.numVertices(), uArray.length(), vArray.length()



def setUVs( mesh ):
    
    uvSetName = "uvSet00"
    
    fnMesh = getMFnMesh( mesh )
    numPolygon = fnMesh.numPolygons()
    
    uArray = om.MFloatArray()
    vArray = om.MFloatArray()

    allLength = 0
    uvCounts = om.MIntArray()
    for i in range( numPolygon ):
        verticesIds = om.MIntArray()
        fnMesh.getPolygonVertices( i, verticesIds )
        allLength += verticesIds.length()
        uvCounts.append( verticesIds.length() )
    
    uArray.setLength( allLength )
    vArray.setLength( allLength )
    
    uvIds = om.MIntArray()
    
    for i in range( numPolygon ):
        verticesIds = om.MIntArray()
        fnMesh.getPolygonVertices( i, verticesIds )
        
        for j in range( verticesIds.length() ):
            rad = math.pi*2 / verticesIds.length() * j
            uPos = math.sin( rad )
            vPos = math.cos( rad )
            
            uArray.set( uPos, verticesIds[j] )
            vArray.set( vPos, verticesIds[j] )
            uvIds.append( verticesIds[j] )
            
    beforeUvCounts = om.MIntArray()
    beforeUvIds = om.MIntArray()
    
    fnMesh.getAssignedUVs( beforeUvCounts, beforeUvIds )
    fnMesh.clearUVs()
    fnMesh.setUV
    fnMesh.assignUVs( uvCounts, uvIds )
    fnMesh.setUVs( uArray, vArray )
    
    for i in range( beforeUvCounts.length() ):
        print "before uvCounts[%d] : %d" %( i, beforeUvCounts[i] )
    for i in range( beforeUvIds.length() ):
        print "before uvIds[%d] : %d" %( i, beforeUvIds[i] )
    
    print "--------------------------------------"
    
    for i in range( uvCounts.length() ):
        print "uvCounts[%d] : %d" %( i, uvCounts[i] )
    for i in range( uvIds.length() ):
        print "uvIds[%d] : %d" %( i, uvIds[i] )