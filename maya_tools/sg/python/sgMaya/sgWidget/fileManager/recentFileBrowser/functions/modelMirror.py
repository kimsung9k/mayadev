import maya.cmds as cmds
import maya.OpenMaya as om



def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj



class MirrorModel:
    
    def __init__(self, baseMesh ):
        
        self.fnMesh = om.MFnMesh( getMObject( baseMesh ) )
        self.points = om.MPointArray()
        
        self.fnMesh.getPoints( self.points )
        self.meshIntersector = om.MMeshIntersector()
        self.meshIntersector.create( self.fnMesh.object() )
        
        pointOnMesh = om.MPointOnMesh()
        
        self.mirrorPointIndices = [ i for i in range( self.points.length() ) ]
        for i in range( self.points.length() ):
            point = self.points[i]
            point.x *= -1
            self.meshIntersector.getClosestPoint( point, pointOnMesh )
            fIndex = pointOnMesh.faceIndex()
            
            intArr = om.MIntArray()
            self.fnMesh.getPolygonVertices( fIndex, intArr )
            
            closeDist = 1000000
            closeIndex = -1
            for j in range( intArr.length() ):
                compairPoint = self.points[ intArr[j] ]
                dist = compairPoint.distanceTo( point )
                if closeDist >= dist:
                    closeDist = dist
                    closeIndex = intArr[j]

            self.mirrorPointIndices[i] = closeIndex
        self.mirrorPoints = om.MPointArray()
        self.mirrorPoints.setLength( self.points.length() )
        
        for i in range( len( self.mirrorPointIndices ) ):
            mirrorIndex = self.mirrorPointIndices[i]
            targetPoint = self.points[mirrorIndex]
            targetPoint.x *= -1
            self.mirrorPoints.set( targetPoint, i )


    def selectMirrorPoint(self, selIndices ):
        
        indices = []
        for sel in selIndices:
            selMeshName = sel.split( '.' )[0]
            index = int( sel.split( '[' )[-1].replace( ']', '' ) )
            mirrorIndex = self.mirrorPointIndices[index]
            indices.append( '%s.vtx[%d]' %(selMeshName,mirrorIndex) )
            
        cmds.select( indices )