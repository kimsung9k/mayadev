import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDag


def getFnMesh( mesh ):
    
    mesh = sgModelDag.getShape( mesh )
    return om.MFnMesh( sgModelDag.getDagPath( mesh ) )


def getMeshNumVertices( mesh ):

    return getFnMesh( mesh ).numVertices()



def getLocalPoints( mesh ):
    
    fnMesh = getFnMesh( mesh )
    points = om.MPointArray()
    fnMesh.getPoints( points )
    return points


def getWorldPoints( mesh ):
    
    fnMesh = getFnMesh( mesh )
    points = om.MPointArray()
    fnMesh.getPoints( points, om.MSpace.kWorld )
    return points



def getMeshAndIndicesPoints( selObjects ):
    
    selObjects = cmds.ls( cmds.polyListComponentConversion( selObjects, tv=1 ), fl=1 )
    
    mesh = ''
    vtxIndices = []
    for obj in selObjects:
        splits = obj.split( '.' )
        if len( splits ) == 1:
            mesh = obj
        else:
            mesh = splits[0]
            index = int( splits[1].split( '[' )[-1].replace( ']', '' ) )
            vtxIndices.append( index )
    
    if vtxIndices:
        vtxIndices = list( set( vtxIndices ) )
    else:
        vtxIndices = [ i for i in range( getFnMesh( mesh ).numVertices() ) ]
    
    return mesh, vtxIndices



class MeshInfo:
    
    def __init__(self, mesh ):
        
        import sgModelDag
        
        fnMesh = om.MFnMesh( sgModelDag.getDagPath( mesh ) )
        
        numVtx  = fnMesh.numVertices()
        numPoly = fnMesh.numPolygons()
        
        verticesPolygons  = []
        polygonsVertices = []
        
        for i in range( numVtx ):
            verticesPolygons.append( om.MIntArray() )
        
        for i in range( numPoly ):
            intArr = om.MIntArray()
            fnMesh.getPolygonVertices( i, intArr )
            polygonsVertices.append( intArr )
            
            for j in range( intArr.length() ):
                vtxIndex = intArr[j]
                faceIndices = verticesPolygons[vtxIndex]
                
                faceIndexExists = False
                for k in range( faceIndices.length() ):
                    if i == faceIndices[k]:
                        faceIndexExists = True
                        break
                if not faceIndexExists:
                    verticesPolygons[vtxIndex].append( i )
        
        self.verticesPolygons = verticesPolygons
        self.polygonsVertices = polygonsVertices
        self.fnMesh = fnMesh
        
        self.verticesCheckList = []
        for i in range( numVtx ):
            self.verticesCheckList.append( False )
        self.numVtx = numVtx
        self.expendLoofVertices = []
            
            
    def resetVerticesCheckList(self):
        
        for i in range( self.numVtx ):
            self.verticesCheckList[i] = False
        
    
    def getExpendVertices(self, vtxIndex ):
        
        faceIndices = self.verticesPolygons[ vtxIndex ]
        
        expendVertices = []
        for i in range( faceIndices.length() ):
            faceIndex = faceIndices[i]
            vertexIndices = self.polygonsVertices[ faceIndex ]
            for j in range( len( vertexIndices ) ):
                vertexIndex = vertexIndices[j]
                if not vertexIndex in expendVertices:
                    expendVertices.append( vertexIndex )
        return expendVertices
    
    
    def getExpendLoof(self, vtxIndex ):
        
        self.resetVerticesCheckList()
        self.expendedVertices = []
        
        def loofArea( vtxIndex ):
            self.expendedVertices.append( vtxIndex )
            self.verticesCheckList[ vtxIndex ] = True
            indices = self.getExpendVertices( vtxIndex )
            for index in indices:
                if not self.verticesCheckList[ index ]:
                    loofArea( index )
        
        loofArea( vtxIndex )
        
        return self.expendedVertices
        
    
    
    def selectExpendVertices(self, vtxIndex ):
        
        indices = self.getExpendVertices( vtxIndex )
        vertices = []
        for i in range( len( indices ) ):
            vertices.append( self.fnMesh.name() + '.vtx[%d]' % indices[i] )
        cmds.select( vertices )