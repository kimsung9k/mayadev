#include "sgGetMeshElementInfo.h"


MStatus getShapeNode( MDagPath& path )
{
	MStatus status;

	if( path.apiType() == MFn::kMesh )
	{
		return MS::kSuccess;
	}

	if( path.apiType() != MFn::kTransform )
	{
		return MS::kFailure;
	}

	unsigned int numShapes;
	path.numberOfShapesDirectlyBelow( numShapes );

	if( !numShapes ) return MS::kFailure;

	for( int i=0; i< numShapes; i++ )
	{
		status = path.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		if( path.apiType() == MFn::kMesh )
		{
			MFnDagNode fnNode = path.node();
			if( !fnNode.isIntermediateObject() )
			{
				return MS::kSuccess;
			}
		}
		path.pop();
	}
	return MS::kFailure;
}


void getGrowSelection( MObject oMesh, sgPolygonPerVertex_array& polygonsPerVertices, int startIndex, MIntArray& idsVertex, MIntArray& chackedVertices )
{
	MFnMesh fnMesh( oMesh );
	MIntArray& faceIndices = polygonsPerVertices[ startIndex ].m_IndicesPolygon;
	MIntArray  vertices;
	MIntArray addVertices;

	if( !chackedVertices.length() ) 
	{
		chackedVertices.setLength( fnMesh.numVertices() );
		for( int i=0; i< chackedVertices.length(); i++ )
		{
			chackedVertices[i] = 0;
		}
	}

	for( int i=0; i< faceIndices.length(); i++ )
	{
		fnMesh.getPolygonVertices( faceIndices[i], vertices );
		for( int j=0; j < vertices.length(); j++ )
		{
			if( chackedVertices[ vertices[j] ] == 0 )
			{
				idsVertex.append( vertices[j] );
				addVertices.append( vertices[j] );
				chackedVertices[ vertices[j] ] = 1;
			}
		}
	}

	if( addVertices.length() )
	{
		for( int i=0; i< addVertices.length(); i++ )
		{
			getGrowSelection( oMesh, polygonsPerVertices, addVertices[i], idsVertex, chackedVertices );
		}
	}
}


MStatus sgGetMeshElementInfo::getInfomationFromSelection()
{
	MStatus status;

	MIntArray resultArrays;
	if( !m_selList.length() ) return MS::kSuccess;

	m_buildMeshDatas.clear();
	sgPolygonPerVertex_array polygonsPerVertices;

	sgBuildMeshData_array  buildMeshDatas;

	MDagPath dagPath;
	status = m_selList.getDagPath( 0, dagPath );
	if( !status ) return MS::kFailure;
	status = getShapeNode( dagPath );
	if( !status ) return MS::kFailure;

	if( dagPath.apiType() != MFn::kMesh ) return MS::kFailure;

	MFnMesh fnMesh( dagPath );
	MPointArray pointsInputMesh;
	fnMesh.getPoints( pointsInputMesh );
	MMatrix mtxMesh = fnMesh.dagPath().inclusiveMatrix();

	int numPolygons = fnMesh.numPolygons();
	int numVertices = fnMesh.numVertices();

	polygonsPerVertices.setLength( numVertices );

	MIntArray verticesCounts;
	MIntArray verticesIds;
	fnMesh.getVertices( verticesCounts,verticesIds );

	for( int i=0; i< numPolygons; i++ )
	{
		MIntArray indices;
		fnMesh.getPolygonVertices( i, indices );
		for( int j=0; j< indices.length(); j++ )
			polygonsPerVertices[ indices[j] ].m_IndicesPolygon.append( i );
	}

	int startIndex = 0;
	MIntArray targetPolygonIndexOn;
	targetPolygonIndexOn.setLength( numPolygons );

	MIntArray checkedVertices;
	checkedVertices.setLength( numVertices );
	for( int i=0; i< checkedVertices.length(); i++ )
		checkedVertices[i] = 0;

	m_buildMeshDatas.clear();

	int whileIndex = 0;
	while( startIndex != -1 )
	{
		MIntArray idsVertex;
		idsVertex.clear();

		getGrowSelection( fnMesh.object(), polygonsPerVertices, startIndex, idsVertex, MIntArray() );

		if( !idsVertex.length() ) break;
		for( int i=0; i< targetPolygonIndexOn.length(); i++ ) targetPolygonIndexOn[i] = 0;
		for( int i=0; i< idsVertex.length(); i++ )
		{
			MIntArray& indicesPolygon = polygonsPerVertices[ idsVertex[i] ].m_IndicesPolygon;
			for( int j=0; j< indicesPolygon.length(); j++ )
			{
				targetPolygonIndexOn[ indicesPolygon[j] ] = 1;
			}
		}

		sgBuildMeshData buildMeshData;
		buildMeshData.m_numVertices = idsVertex.length();

		MIntArray sortIndices;
		sortIndices.append( idsVertex[0] );
		for( int i=1; i< idsVertex.length(); i++ )
		{
			bool isInserted = false;
			for( int j=0; j< sortIndices.length(); j++ )
			{
				if( sortIndices[j] > idsVertex[i] )
				{
					sortIndices.insert( idsVertex[i], j );
					isInserted = true;
					break;
				}
			}
			if( isInserted ) continue;
			sortIndices.append( idsVertex[i] );
		}

		MIntArray sortIndicesMap;
		sortIndicesMap.setLength( numVertices );
		for( int i=0; i< sortIndicesMap.length(); i++ )
		{
			sortIndicesMap[i] = -1;
		}
		for( int i=0; i< sortIndices.length(); i++ )
		{
			sortIndicesMap[ sortIndices[i] ] = i;
		}

		buildMeshData.m_points.setLength( buildMeshData.m_numVertices );
		for( int i=0; i< buildMeshData.m_numVertices; i++ )
		{
			buildMeshData.m_points[i] = pointsInputMesh[ sortIndices[i] ] * mtxMesh;
		}

		buildMeshData.m_numPolygons = 0;
		buildMeshData.m_originalFaceIndices.clear();
		for( int i=0; i< targetPolygonIndexOn.length(); i++ )
		{
			if( !targetPolygonIndexOn[i] ) continue;
			buildMeshData.m_vertexCount.append( verticesCounts[ i ] );
			buildMeshData.m_originalFaceIndices.append( i );
			buildMeshData.m_numPolygons++;
			MIntArray indicesVertices;
			fnMesh.getPolygonVertices( i, indicesVertices );
			for( int j=0; j< indicesVertices.length(); j++ )
				buildMeshData.m_vertexList.append( sortIndicesMap[indicesVertices[j]] );
		}
		m_buildMeshDatas.append( buildMeshData );

		for( int i =0; i< idsVertex.length(); i++ )
			checkedVertices[ idsVertex[i] ] = 1;

		startIndex = -1;
		for( int i=0; i< checkedVertices.length(); i++ )
		{
			if( checkedVertices[i] == 1 ) continue;
			startIndex = i;
			break;
		}
	}

	return MS::kSuccess;
}