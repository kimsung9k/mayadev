#include "sgBuildMeshData.h"

sgBuildMeshData::sgBuildMeshData()
{
	m_numVertices = 0;
	m_numPolygons = 0;
};
sgBuildMeshData::~sgBuildMeshData(){};

void sgBuildMeshData::clear()
{
	m_numVertices = 0;
	m_numPolygons = 0;
	m_points.clear();
	m_vertexCount.clear();
	m_vertexList.clear();
	m_originalFaceIndices.clear();
}

void sgBuildMeshData::appendMeshData( const MObject& oMesh, MMatrix mtxMesh )
{
	MFnMesh fnMesh( oMesh );

	MPointArray points, keepPoints;
	MIntArray   vtxCount, keepVtxCount;
	MIntArray   vtxList, keepVtxList;

	keepPoints   = m_points;
	keepVtxCount = m_vertexCount;
	keepVtxList  = m_vertexList;


	fnMesh.getPoints( points );
	fnMesh.getVertices( vtxCount, vtxList );

	int startIndexPoints = m_points.length();
	int startIndexVtxCount = m_vertexCount.length();
	int startIndexVtxList  = m_vertexList.length();
		
	m_numVertices += fnMesh.numVertices();
	m_numPolygons += fnMesh.numPolygons();

	m_points.setLength( startIndexPoints + points.length() );
	for( unsigned int i=0; i< points.length(); i++ )
	{
		m_points[ i + startIndexPoints ] = points[i] * mtxMesh;
	}
	m_vertexCount.setLength( startIndexVtxCount + vtxCount.length() );
	for( unsigned int i=0; i< vtxCount.length(); i++ )
	{
		m_vertexCount[ i + startIndexVtxCount ] = vtxCount[i];
	}
	m_vertexList.setLength( startIndexVtxList + vtxList.length() );
	for( unsigned int i=0; i< vtxList.length(); i++ )
	{
		m_vertexList[ i + startIndexVtxList ] = vtxList[i] + startIndexPoints;
	}
}


void sgBuildMeshData::appendMeshData( const sgBuildMeshData& meshData )
{
	MPointArray points   = meshData.m_points;
	MIntArray   vtxCount = meshData.m_vertexCount;
	MIntArray   vtxList  = meshData.m_vertexList;

	int startIndexPoints   = m_points.length();
	int startIndexVtxCount = m_vertexCount.length();
	int startIndexVtxList  = m_vertexList.length();

	m_numVertices += meshData.m_numVertices;
	m_numPolygons += meshData.m_numPolygons;

	m_points.setLength( startIndexPoints + points.length() );
	for( unsigned int i=0; i< points.length(); i++ )
	{
		m_points[ i + startIndexPoints ] = points[i];
	}
	m_vertexCount.setLength( startIndexVtxCount + vtxCount.length() );
	for( unsigned int i=0; i< vtxCount.length(); i++ )
	{
		m_vertexCount[ i + startIndexVtxCount ] = vtxCount[i];
	}
	m_vertexList.setLength( startIndexVtxList + vtxList.length() );
	for( unsigned int i=0; i< vtxList.length(); i++ )
	{
		m_vertexList[ i + startIndexVtxList ] = vtxList[i] + startIndexPoints;
	}
}

void   sgBuildMeshData::getPositon( MObject oMesh, MMatrix mtxMesh, int startIndex )
{
	MPointArray points;
	MFnMesh fnMesh;
	fnMesh.setObject( oMesh );
	fnMesh.getPoints( points );

	for( unsigned int i=0; i< points.length(); i++ )
	{
		m_points[ i + startIndex ] = points[i] * mtxMesh;
	}
}


void sgBuildMeshData::setPosition()
{
	MFnMesh fnMesh;
	fnMesh.setObject( m_oMesh );
	fnMesh.setPoints( m_points );
	fnMesh.updateSurface();
}


void sgBuildMeshData::operator=( const sgBuildMeshData& meshData )
{
	m_oMesh       = meshData.m_oMesh;
	m_numVertices = meshData.m_numVertices;
	m_numPolygons = meshData.m_numPolygons;
	m_points      = meshData.m_points;
	m_vertexCount = meshData.m_vertexCount;
	m_vertexList  = meshData.m_vertexList;
	m_pOriginalPoints         = meshData.m_pOriginalPoints;
	m_originalVerticesIndices = meshData.m_originalVerticesIndices;
	m_originalFaceIndices     = meshData.m_originalFaceIndices;
	m_appendedIndices         = meshData.m_appendedIndices;

	m_inputMeshIndex = meshData.m_inputMeshIndex;
}



MStatus sgBuildMeshData::build()
{
	MStatus status;

	MFnMesh fnMesh;
	MFnMeshData meshData;
	m_oMesh = meshData.create();
	/*
	cout << "build start : " << endl;
	cout << "/////////////////////////////////////////////" << endl;
	cout << "num vertices : " << m_numVertices << endl;
	cout << "num polygons : " << m_numPolygons << endl;
	for( unsigned int i=0; i< m_points.length(); i++ )
	{
		printf( "point[%d] : %5.2f, %5.2f, %5.2f\n", i, m_points[i].x, m_points[i].y, m_points[i].z ); 
	}
	cout << endl;
	for( unsigned int i=0; i< m_vertexCount.length(); i++ )
	{
		printf( "vtxCount[%d] : %d\n", i, m_vertexCount[i] ); 
	}
	cout << endl;
	for( unsigned int i=0; i< m_vertexList.length(); i++ )
	{
		printf( "vtxList[%d] : %d\n", i, m_vertexList[i] ); 
	}
	cout << "/////////////////////////////////////////////" << endl;
	cout << "build end : " << endl;
	*/

	fnMesh.create( m_numVertices, m_numPolygons, m_points, 
		m_vertexCount, m_vertexList, m_oMesh );

	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}



sgBuildMeshData_array::sgBuildMeshData_array()
{
	m_length = 0;
	m_pSgBuildMeshData = new sgBuildMeshData[0];
}


sgBuildMeshData_array::~sgBuildMeshData_array()
{
	delete[] m_pSgBuildMeshData;
}


unsigned int sgBuildMeshData_array::length()
{
	return m_length;
}


void sgBuildMeshData_array::clear()
{
	for( unsigned int i=0; i< m_length; i++ )
	{
		m_pSgBuildMeshData[i].clear();
	}
	delete[] m_pSgBuildMeshData;
	m_length = 0;
	m_pSgBuildMeshData = new sgBuildMeshData[0];
}


void sgBuildMeshData_array::setLength( unsigned int length )
{
	for( unsigned int i=0; i< m_length; i++ )
	{
		m_pSgBuildMeshData[i].clear();
	}
	delete[] m_pSgBuildMeshData;
	m_length = length;
	m_pSgBuildMeshData = new sgBuildMeshData[length];
}


sgBuildMeshData& sgBuildMeshData_array::operator[]( unsigned int index ) const
{
	return m_pSgBuildMeshData[ index ];
}


void sgBuildMeshData_array::operator=( const sgBuildMeshData_array& meshData_array )
{
	for( unsigned int i=0; i< m_length; i++ )
	{
		m_pSgBuildMeshData[i].clear();
	}
	delete[] m_pSgBuildMeshData;

	m_length = meshData_array.m_length;
	m_pSgBuildMeshData = new sgBuildMeshData[ m_length ];
	for( unsigned int i=0; i< m_length; i++ )
	{
		m_pSgBuildMeshData[i] = meshData_array[i];
	}
}



void sgBuildMeshData_array::append( const sgBuildMeshData& meshData )
{
	sgBuildMeshData* pTemp = m_pSgBuildMeshData;

	m_pSgBuildMeshData = new sgBuildMeshData[ m_length + 1 ];
	
	for( unsigned int i=0; i< m_length; i++ )
		m_pSgBuildMeshData[i] = pTemp[i];
	m_pSgBuildMeshData[m_length] = meshData;
	m_length += 1;

	delete[] pTemp;
}








sgPolygonPerVertex::sgPolygonPerVertex()
{
	m_IndicesPolygon.clear();
}

sgPolygonPerVertex::~sgPolygonPerVertex()
{
}


sgPolygonPerVertex_array::sgPolygonPerVertex_array()
{
	m_pPolygonPerVertex = new sgPolygonPerVertex[0];
	m_length = 0;
}


sgPolygonPerVertex_array::~sgPolygonPerVertex_array()
{
	delete[] m_pPolygonPerVertex;
}

void sgPolygonPerVertex_array::clear()
{
	delete[] m_pPolygonPerVertex;
	m_pPolygonPerVertex = new sgPolygonPerVertex[0];
	m_length = 0;
}


void sgPolygonPerVertex_array::setLength( unsigned int length )
{
	delete[] m_pPolygonPerVertex;
	m_pPolygonPerVertex = new sgPolygonPerVertex[length];
	m_length = length;
}

unsigned int sgPolygonPerVertex_array::length()
{
	return m_length;
}

sgPolygonPerVertex& sgPolygonPerVertex_array::operator[]( unsigned int index ) const
{
	return m_pPolygonPerVertex[ index ];
}