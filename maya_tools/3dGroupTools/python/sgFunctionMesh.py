import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDag
import sgModelDg


class MeshMirror:
    
    def __init__(self, meshName = '' ):
        
        if meshName:
            self.setBaseMesh( meshName )


    def setBaseMesh(self, meshName ):
        
        meshName = sgModelDag.getShape( meshName )
        oMesh = sgModelDg.getMObject( meshName )
        
        intersector = om.MMeshIntersector()
        fnMesh = om.MFnMesh()
        
        intersector.create( oMesh )
        fnMesh.setObject( oMesh )
        
        pointsMesh = om.MPointArray()
        
        fnMesh.getPoints( pointsMesh )
        
        self.mirrorIndices = om.MIntArray()
        self.mirrorIndices.setLength( pointsMesh.length() )
        for i in range( self.mirrorIndices.length() ):
            self.mirrorIndices[i] = -1
        
        pointOnMesh = om.MPointOnMesh()
        indicesVertices = om.MIntArray()
        
        for i in range( pointsMesh.length() ):
            if self.mirrorIndices[i] != -1: continue
            
            mirrorPoint = om.MPoint( -pointsMesh[i].x, pointsMesh[i].y, pointsMesh[i].z )
            intersector.getClosestPoint( mirrorPoint, pointOnMesh )
            faceIndex = pointOnMesh.faceIndex()
            fnMesh.getPolygonVertices( faceIndex, indicesVertices )
            
            minDist = 10000000.0
            minDistIndex = 0
            for j in range( indicesVertices.length() ):
                dist = mirrorPoint.distanceTo( pointsMesh[ indicesVertices[j] ] )
                if dist < minDist:
                    minDist = dist
                    minDistIndex = indicesVertices[j]
            self.mirrorIndices[i] = minDistIndex
            
            self.mirrorIndices[i] = minDistIndex
            self.mirrorIndices[minDistIndex] = i
        
        self.points = pointsMesh
        self.meshName = meshName
        

    def flip(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgModelDag.getDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def mirror_L_to_R(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgModelDag.getDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            
            if points[i].x < 0: continue
            
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def mirror_R_to_L(self, meshName ):
        
        points = om.MPointArray()
        fnMesh = om.MFnMesh( sgModelDag.getDagPath( meshName ) )
        fnMesh.getPoints( points )
        
        for i in range( points.length() ):
            
            if points[i].x > 0: continue
            
            mirrorIndex = self.mirrorIndices[i]
            targetPoint = points[ mirrorIndex ]
            
            cmds.move( -targetPoint.x, targetPoint.y, targetPoint.z, meshName+'.vtx[%d]' % i, os=1 )
    
    
    def selectLeftIndices(self, meshName, tol=0.001 ):
        
        import math
        leftIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x < 0:
                leftIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( leftIndices )
    
    
    def selectRightIndices(self, meshName, tol=0.001 ):
        
        import math
        rightIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x > 0:
                rightIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( rightIndices )
    
    
    def selectCenterIndices(self, meshName, tol=0.001 ):
        
        import math
        centerIndices = []
        
        for i in range( self.points.length() ):
            if not math.fabs( self.points[i].x ) < tol: continue
            centerIndices.append( meshName+'.vtx[%d]' % i )
        
        cmds.select( centerIndices )
    
    
    def getLeftIndices(self, meshName, tol=0.001 ):
        
        import math
        leftIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x < 0:
                leftIndices.append( i )
        
        return leftIndices
    
    
    def getRightIndices(self, meshName, tol=0.001 ):
        
        import math
        rightIndices = []
        
        for i in range( self.points.length() ):
            if math.fabs( self.points[i].x ) < tol: continue
            if self.points[i].x > 0:
                rightIndices.append( i )
        
        return rightIndices
    
    
    def getCenterIndices(self, meshName, tol=0.001 ):
        
        import math
        centerIndices = []
        
        for i in range( self.points.length() ):
            if not math.fabs( self.points[i].x ) < tol: continue
            centerIndices.append(  i )
        
        return centerIndices
    




def MeshSetClosestPoint( baseName, targetName ):
        
    baseName = sgModelDag.getShape( baseName )
    oBase = sgModelDg.getMObject( baseName )
    
    intersector = om.MMeshIntersector()
    fnMeshBase = om.MFnMesh( oBase )
    intersector.create( oBase )
    
    pointsBase = om.MPointArray()
    fnMeshBase.getPoints( pointsBase )
    
    dagPathTarget = sgModelDag.getDagPath( targetName )
    fnMeshTarget = om.MFnMesh( dagPathTarget )
    
    pointsTarget = om.MPointArray()
    fnMeshTarget.getPoints( pointsTarget )
    
    pointOnMesh = om.MPointOnMesh()
    indicesVtx = om.MIntArray()
    for i in range( pointsTarget.length() ):
        intersector.getClosestPoint( pointsTarget[i], pointOnMesh )
        faceIndex = pointOnMesh.faceIndex()
        fnMeshBase.getPolygonVertices( faceIndex, indicesVtx )
        
        closeDist = 1000000.0
        closeIndex = 0
        for j in range( indicesVtx.length() ):
            dist = pointsTarget[i].distanceTo( pointsBase[ indicesVtx[j] ] )
            if dist < closeDist:
                closeDist = dist
                closeIndex = indicesVtx[j]
        
        pointBase = pointsBase[ closeIndex ]
        cmds.move( pointBase.x, pointBase.y, pointBase.z, targetName+'.vtx[%d]' % i, os=1 )
        


def cleanMesh( meshObj ):
    
    shapes = cmds.listRelatives( meshObj, s=1, f=1 )
    
    for shape in shapes:
        if not cmds.getAttr( shape+'.io' ): continue
        if cmds.listConnections( shape ): continue
        cmds.delete( shape )
        cmds.warning( '"%s" shape is deleted' % shape )




def createMeshData( targetMesh, path ):
    
    import cPickle
    pass




def buildMeshFromData( path ):
    
    import cPickle
    pass