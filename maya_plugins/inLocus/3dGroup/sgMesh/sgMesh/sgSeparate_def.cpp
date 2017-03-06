#include "sgSeparate.h"


void sgSeparate::getGrowSelection( MObject oMesh, const sgPolygonPerVertex_array& polygonsPerVertices,
	             int startIndex, MIntArray& idsVertex, MIntArray& chackedVertices )
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
			if( !idsVertex.length() )break;
		}
	}
}



MStatus sgSeparate::separateEachElement( MObject oMesh, int index )
{
	MStatus status;

	MFnMesh fnMesh( oMesh );
	MPointArray pointsInputMesh;
	fnMesh.getPoints( pointsInputMesh );
	MMatrix mtxMesh = fnMesh.dagPath().inclusiveMatrix();

	sgPolygonPerVertex_array polygonsPerVertices;

	int numPolygons = fnMesh.numPolygons();
	int numVertices = fnMesh.numVertices();

	polygonsPerVertices.setLength( numVertices );

	MIntArray verticesCounts;
	fnMesh.getVertices( verticesCounts,MIntArray() );

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

	while( startIndex != -1 )
	{
		MIntArray idsVertex;
		idsVertex.clear();

		getGrowSelection( oMesh, polygonsPerVertices, startIndex, idsVertex, MIntArray() );

		if( !idsVertex.length() )break;
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
		buildMeshData.m_inputMeshIndex = index;
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
		buildMeshData.m_originalVerticesIndices.setLength( buildMeshData.m_numVertices );
		for( int i=0; i< buildMeshData.m_numVertices; i++ )
		{
			buildMeshData.m_originalVerticesIndices[i] = sortIndices[i];
			buildMeshData.m_points[i] = pointsInputMesh[ sortIndices[i] ] * mtxMesh;
		}

		buildMeshData.m_numPolygons = 0;
		for( int i=0; i< targetPolygonIndexOn.length(); i++ )
		{
			if( !targetPolygonIndexOn[i] ) continue;
			buildMeshData.m_vertexCount.append( verticesCounts[ i ] );
			buildMeshData.m_numPolygons++;
			MIntArray indicesVertices;
			fnMesh.getPolygonVertices( i, indicesVertices );
			for( int j=0; j< indicesVertices.length(); j++ )
				buildMeshData.m_vertexList.append( sortIndicesMap[indicesVertices[j]] );
		}
		m_meshDataArray.append( buildMeshData );

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




MStatus sgSeparate::setThread()
{
	int numThread = NUM_THREAD;
	int outputLength = m_meshDataArray_output.length();

	if( outputLength < numThread )
		numThread = outputLength;

	int eachLength = outputLength/numThread;
	int restLength = outputLength - eachLength*numThread;

	m_pThread = new sgSeparate_ThreadData[ numThread ];

	char szBuff[512];
	sprintf( szBuff, "start thread" );
	OutputDebugString(szBuff);

	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			m_pThread[i].start = start;
			m_pThread[i].end   = start+eachLength+1;
		}
		else
		{
			m_pThread[i].start = start;
			m_pThread[i].end   = start+eachLength;
		}
		m_pThread[i].numThread = numThread;
		m_pThread[i].pTask     = m_pTask;
		start = m_pThread[i].end;

		sprintf( szBuff, "start : %d, end : %d\n", m_pThread[i].start, m_pThread[i].end );
		OutputDebugString(szBuff);
	}
	
	return MS::kSuccess;
}


MStatus sgSeparate::endThread()
{
	delete []m_pThread;
	return MS::kSuccess;
}



void sgSeparate::parallelCompute_build( void* data, MThreadRootTask *pRoot )
{
	sgSeparate_ThreadData* pThread = (sgSeparate_ThreadData*)data;

	for( int i=0; i< pThread->numThread; i++ )
	{
		MThreadPool::createTask( threadCompute_build, (void*)&pThread[i], pRoot );
	}
	MThreadPool::executeAndJoin( pRoot );
}


MThreadRetVal sgSeparate::threadCompute_build( void* pData )
{
	sgSeparate_ThreadData* pThread = ( sgSeparate_ThreadData* )pData;
	sgSeparate_TaskData*   pTask =  pThread->pTask;
	sgBuildMeshData_array& meshDataArray = *pTask->m_pMeshDataArray_output;

	for( unsigned int i= pThread->start; i< pThread->end; i++ )
	{
		meshDataArray[i].build();
	}

	return (MThreadRetVal)0;
}



void sgSeparate::parallelCompute_setPosition( void* data, MThreadRootTask *pRoot )
{
	sgSeparate_ThreadData* pThread = (sgSeparate_ThreadData*)data;

	for( int i=0; i< pThread->numThread; i++ )
	{
		MThreadPool::createTask( threadCompute_setPosition, (void*)&pThread[i], pRoot );
	}
	MThreadPool::executeAndJoin( pRoot );
}


MThreadRetVal sgSeparate::threadCompute_setPosition( void* pData )
{
	sgSeparate_ThreadData* pThread = ( sgSeparate_ThreadData* )pData;
	sgSeparate_TaskData*   pTask =  pThread->pTask;

	MMatrixArray& mtxArrInput = *pTask->m_pMtxArrInput;
	vector<MPointArray> pointArraysInput = *pTask->m_pPointArraysInput;
	sgBuildMeshData_array& meshDataArray_input = *pTask->m_pMeshDataArray_input;
	sgBuildMeshData_array& meshDataArray_output = *pTask->m_pMeshDataArray_output;

	unsigned int index = pThread->start;

	int numVertices_output = 0;
	sgBuildMeshData& meshData_output = meshDataArray_output[index];
	MIntArray& appendedIndices = meshData_output.m_appendedIndices;

	for( int j=0; j< appendedIndices.length(); j++ )
	{
		int appendedIndex = meshData_output.m_appendedIndices[j];
		sgBuildMeshData& targetMeshData = meshDataArray_input[ appendedIndex ];

		int numVertices = targetMeshData.m_numVertices;
		numVertices_output += numVertices;
	}
	MFnMesh fnMesh;
	int currentIndex = 0;
	MIntArray& originalIndices = meshData_output.m_appendedIndices;
	MPointArray& pointArray_output = meshData_output.m_points;

	for( int j=0; j< originalIndices.length(); j++ )
	{
		int appendedIndex = originalIndices[j];
		sgBuildMeshData& meshData_input = meshDataArray_input[ appendedIndex ];
		int inputMeshIndex = meshData_input.m_inputMeshIndex;
			
		fnMesh.setObject( meshData_input.m_oMesh );
		MMatrix mtxMesh = fnMesh.dagPath().inclusiveMatrix();
		MMatrix& mtxInputMesh = mtxArrInput[ inputMeshIndex ];
		MPointArray& basePoints = pointArraysInput[ inputMeshIndex ];

		MIntArray&   verticeIndices = meshData_input.m_originalVerticesIndices;
		for( int k=0; k< verticeIndices.length(); k++ )
		{
			pointArray_output[ currentIndex ] = basePoints[ verticeIndices[k] ] * mtxInputMesh;
			currentIndex++;
		}
	}
	MFnMesh fnMesh_output( meshData_output.m_oMesh );
	fnMesh_output.setPoints( pointArray_output );


	return (MThreadRetVal)0;
}