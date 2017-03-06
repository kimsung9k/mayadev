#include "slidingDeformer2.h"


void slidingDeformer2::check_time_start()
{
	if (m_condition = QueryPerformanceFrequency((_LARGE_INTEGER*)&m_freq))  QueryPerformanceCounter((_LARGE_INTEGER*)&m_start);
}



void slidingDeformer2::check_time_end( float& a, bool& b )
{
	if (m_condition) {QueryPerformanceCounter((_LARGE_INTEGER*)&m_end);  a=(float)((double)(m_end - m_start)/m_freq*1000); b=TRUE;}
	else b=FALSE;
}



void slidingDeformer2::setThread_chkIndices()
{
	m_pTaskChkIndices->pPointsMoved   = &m_pointsMoved;
	m_pTaskChkIndices->pPointsOrig    = &m_pointsOrig;
	MIntDoubleArray& indicesThread   = m_pTaskChkIndices->IndicesThread;
	m_pTaskChkIndices->pIndicesMoved  = &m_indicesMoved;

	int numThread = m_numThread;
	int meshPointLength = m_pointsOrig.length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;
	indicesThread.setLength( numThread );
	
	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			m_pThreadChkIndices[i].start = start;
			m_pThreadChkIndices[i].end   = start+eachLength+1;
		}
		else
		{
			m_pThreadChkIndices[i].start = start;
			m_pThreadChkIndices[i].end   = start+eachLength;
		}
		m_pThreadChkIndices[i].numThread = numThread;
		m_pThreadChkIndices[i].pTask = m_pTaskChkIndices;
		m_pThreadChkIndices[i].threadIndex = i;
		indicesThread[i].setLength( m_pThreadChkIndices[i].end - m_pThreadChkIndices[i].start );
		start = m_pThreadChkIndices[i].end;
	}
}


MThreadRetVal slidingDeformer2::compute_chkIndices( void* voidPThread )
{
	slidingDeformer2ChkIndicesThread* pThread = ( slidingDeformer2ChkIndicesThread* )voidPThread;
	slidingDeformer2ChkIndicesTask*   pTask   = pThread->pTask;
	MIntArray& threadedIndices = pTask->IndicesThread[ pThread->threadIndex ];
	
	MPointArray&  pointsMoved = *pTask->pPointsMoved;
	MPointArray&  pointsOrig  = *pTask->pPointsOrig;

	int loofLength = pThread->end - pThread->start;
	threadedIndices.setLength( loofLength );

	int addNum = 0;
	for( int i=pThread->start; i< pThread->end; i++ )
	{
		if( fabs( pointsOrig[i].x - pointsMoved[i].x ) > 0.0001 )
		{
			threadedIndices[ addNum++ ] = i;
		}
		else if( fabs( pointsOrig[i].y - pointsMoved[i].y ) > 0.0001 )
		{
			threadedIndices[ addNum++ ] = i;
		}
		else if( fabs( pointsOrig[i].y - pointsMoved[i].y ) > 0.0001 )
		{
			threadedIndices[ addNum++ ] = i;
		}
	}
	threadedIndices.setLength( addNum );
	
	return MThreadRetVal( 0 );
}


void slidingDeformer2::parallelCompute_chkIndices( void* data, MThreadRootTask * pRoot )
{
	slidingDeformer2ChkIndicesThread* pThread = ( slidingDeformer2ChkIndicesThread* )data;

	if( pThread )
	{
		for( int i=0; i<pThread->numThread; i++ )
		{
			MThreadPool::createTask( compute_chkIndices, ( void* )&pThread[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}



void slidingDeformer2::endThread_chkIndices()
{
	int allLength=0;
	for( int i=0; i< m_pTaskChkIndices->IndicesThread.length; i++ )
	{
		allLength += m_pTaskChkIndices->IndicesThread[i].length();
	}
	m_indicesMoved.setLength( allLength );

	int addNum = 0;
	for( int i=0; i< m_pTaskChkIndices->IndicesThread.length; i++ )
	{
		for( unsigned int j=0; j<m_pTaskChkIndices->IndicesThread[i].length(); j++ )
		{
			m_indicesMoved[ addNum++ ] = m_pTaskChkIndices->IndicesThread[i][j];
		}
	}
}



MStatus slidingDeformer2::checkDeformedVertices()
{
	MStatus status;

	if( !m_checkAllPoints )
	{
		setThread_chkIndices();
		MThreadPool::newParallelRegion( parallelCompute_chkIndices, m_pThreadChkIndices );
		endThread_chkIndices();

		m_pIndicesCheck = &m_indicesMoved;
	}
	else
	{
		m_pIndicesCheck = &m_indicesAllPoints;
	}

	return MS::kSuccess;
}


/*
MStatus slidingDeformer2::checkDeformedVertices( const MPointArray& basePoints, const MPointArray& movedPoints,
	                                            MIntArray& movedIndices )
{
	MStatus status;
	
	int basePointLength = basePoints.length();
	movedIndices.setLength( basePointLength );

	int addNum = 0;
	for( int i=0; i< basePointLength; i++ )
	{
		bool xDiff = fabs( basePoints[i].x - movedPoints[i].x ) > 0.0001;
		bool yDiff = fabs( basePoints[i].y - movedPoints[i].y ) > 0.0001;
		bool zDiff = fabs( basePoints[i].z - movedPoints[i].z ) > 0.0001;

		if( xDiff || yDiff || zDiff )
		{
			movedIndices[ addNum++ ] = i;
		}
	}
	movedIndices.setLength( addNum );
	return MS::kSuccess;
}
*/



void slidingDeformer2::setThread_getDist()
{
	m_pTaskGetDist->pMeshIntersector = m_pMeshIntersector;
	m_pTaskGetDist->pPointsOrig      = &m_pointsOrig;
	m_pTaskGetDist->pVectors         = &m_vectorArr;

	int numThread = m_numThread;
	int meshPointLength = m_pointsOrig.length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;
	
	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			m_pThreadGetDist[i].start = start;
			m_pThreadGetDist[i].end   = start+eachLength+1;
		}
		else
		{
			m_pThreadGetDist[i].start = start;
			m_pThreadGetDist[i].end   = start+eachLength;
		}
		m_pThreadGetDist[i].numThread = numThread;
		m_pThreadGetDist[i].pTask = m_pTaskGetDist;
		start = m_pThreadGetDist[i].end;
	}
}



MThreadRetVal slidingDeformer2::compute_getDist( void* voidPThread )
{
	slidingDeformer2GetDistThread* pThread = ( slidingDeformer2GetDistThread* )voidPThread;
	slidingDeformer2GetDistTask*   pTask   = pThread->pTask;
	
	MPointOnMesh  pointOnMesh;
	MVectorArray& vectorArr   = *pTask->pVectors;
	MPointArray&  pointsOrig = *pTask->pPointsOrig;

	MVector vPoint;
	MVector getPoint;
	MVector normal;
	double dot;
	for( int i = pThread->start; i < pThread->end; i++ )
	{
		pTask->pMeshIntersector->getClosestPoint( pointsOrig[i], pointOnMesh );
		getPoint = pointOnMesh.getPoint();
		vectorArr[i] = MVector( pointsOrig[i] ) - getPoint;
	}
	return MThreadRetVal( 0 );
}


void slidingDeformer2::parallelCompute_getDist( void* data, MThreadRootTask * pRoot )
{
	slidingDeformer2SlidingThread* pThread = ( slidingDeformer2SlidingThread* )data;

	if( pThread )
	{
		for( int i=0; i<pThread->numThread; i++ )
		{
			MThreadPool::createTask( compute_getDist, ( void* )&pThread[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}


void slidingDeformer2::endThread_getDist()
{
}


MStatus slidingDeformer2::getSlidingDistance()
{
	MStatus status;

	setThread_getDist();
	MThreadPool::newParallelRegion( parallelCompute_getDist, m_pThreadGetDist );
	endThread_getDist();

	return MS::kSuccess;
}


void slidingDeformer2::setThread_sliding()
{
	m_pTaskSliding->env              = m_env;
	m_pTaskSliding->pMeshIntersector = m_pMeshIntersector;
	m_pTaskSliding->pPointsMoved     = &m_pointsMoved;
	m_pTaskSliding->pPointsResult    = &m_pointsResult;
	m_pTaskSliding->pVectorArr       = &m_vectorArr;
	m_pTaskSliding->pIndicesCheck    = m_pIndicesCheck;

	int numThread = m_numThread;
	int meshPointLength = m_pIndicesCheck->length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;
	
	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			m_pThreadSliding[i].start = start;
			m_pThreadSliding[i].end   = start+eachLength+1;
		}
		else
		{
			m_pThreadSliding[i].start = start;
			m_pThreadSliding[i].end   = start+eachLength;
		}
		m_pThreadSliding[i].numThread = numThread;
		m_pThreadSliding[i].pTask = m_pTaskSliding;
		start = m_pThreadSliding[i].end;
	}
}


MThreadRetVal slidingDeformer2::compute_sliding( void* voidPThread )
{
	slidingDeformer2SlidingThread* pThread = ( slidingDeformer2SlidingThread* )voidPThread;
	slidingDeformer2SlidingTask*   pTask   = pThread->pTask;
	
	MPointOnMesh	pointOnMesh;
	MIntArray& indicesMoved = *pTask->pIndicesCheck;
	MPointArray& pointsMoved  = *pTask->pPointsMoved;
	MPointArray& pointsResult = *pTask->pPointsResult;
	MVectorArray& vectorArr   = *pTask->pVectorArr;

	MPoint pointClose;
	MVector normal;
	int index;

	float env    = pTask->env;
	float invEnv = 1-pTask->env;

	for( int i = pThread->start; i < pThread->end; i++ )
	{
		index = indicesMoved[i];
		pTask->pMeshIntersector->getClosestPoint( pointsMoved[ index ], pointOnMesh );
		pointClose = pointOnMesh.getPoint();
		pointsResult[ index ] = vectorArr[index] + pointClose*env + pointsMoved[ index ]*invEnv;
	}
	return MThreadRetVal( 0 );
}

void slidingDeformer2::parallelCompute_sliding( void* data, MThreadRootTask * pRoot )
{
	slidingDeformer2SlidingThread* pThread = ( slidingDeformer2SlidingThread* )data;

	if( pThread )
	{
		for( int i=0; i<pThread->numThread; i++ )
		{
			MThreadPool::createTask( compute_sliding, ( void* )&pThread[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}

void slidingDeformer2::endThread_sliding()
{
}


MStatus slidingDeformer2::sliding()
{
	MStatus status;

	setThread_sliding();
	MThreadPool::newParallelRegion( parallelCompute_sliding, m_pThreadSliding );
	endThread_sliding();

	return MS::kSuccess;
}