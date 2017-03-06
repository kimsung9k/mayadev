#include "sgSlidingDeformer.h"



void sgSlidingDeformer::check_time_start()
{
	if (m_condition = QueryPerformanceFrequency((_LARGE_INTEGER*)&m_freq))  QueryPerformanceCounter((_LARGE_INTEGER*)&m_start);
}


void sgSlidingDeformer::check_time_end( float& a, bool& b )
{
	if (m_condition) {QueryPerformanceCounter((_LARGE_INTEGER*)&m_end);  a=(float)((double)(m_end - m_start)/m_freq*1000); b=TRUE;}
	else b=FALSE;
}


MStatus sgSlidingDeformer::checkDeformedVertices( const MPointArray& basePoints, const MPointArray& movedPoints,
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


void sgSlidingDeformer::setThread()
{
	m_pTask->pMeshIntersector = m_pMeshIntersector;
	m_pTask->pPointsMoved     = &m_pointsMoved;
	m_pTask->pPointsBase      = &m_pointsBase;
	m_pTask->pIndicesMoved    = &m_indicesMoved;

	int numThread = m_numThread;
	int meshPointLength = m_indicesMoved.length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;
	
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
		m_pThread[i].pTask = m_pTask;
		start = m_pThread[i].end;
	}
}

MThreadRetVal sgSlidingDeformer::deformCompute( void* voidPThread )
{
	sgSlidingDeformerThread* pThread = ( sgSlidingDeformerThread* )voidPThread;
	sgSlidingDeformerTask*   pTask   = pThread->pTask;
	
	MPointOnMesh  pointOnMeshBase, pointOnMeshMoved;
	MIntArray&    indicesMoved = *pTask->pIndicesMoved;
	MPointArray&  pointsMoved = *pTask->pPointsMoved;
	MPointArray&  pointsBase  = *pTask->pPointsBase;

	for( int i = pThread->start; i < pThread->end; i++ )
	{
		pTask->pMeshIntersector->getClosestPoint( pointsBase[ indicesMoved[i] ], pointOnMeshBase );

		MPoint  pClosePoint = pointOnMeshBase.getPoint();
		MVector vDiff  = pointsBase[ indicesMoved[i] ] - pClosePoint;
		MVector normal = pointOnMeshBase.getNormal();
		MVector vMove = pointsMoved[ indicesMoved[i] ] - pointsBase[ indicesMoved[i] ];
		MVector proj = ( vMove * normal ) / ( pow( normal.x, 2 ) + pow( normal.y, 2 ) + pow( normal.z, 2 ) ) * normal;
		MPoint  pCompair = vMove - proj + pointsBase[ indicesMoved[i] ];

		pTask->pMeshIntersector->getClosestPoint( pCompair, pointOnMeshMoved );
		pointsMoved[ indicesMoved[i] ] = vDiff + pointOnMeshMoved.getPoint();
	}
	return MThreadRetVal( 0 );
}

void sgSlidingDeformer::parallelCompute( void* data, MThreadRootTask * pRoot )
{
	sgSlidingDeformerThread* pThread = ( sgSlidingDeformerThread* )data;

	if( pThread )
	{
		for( int i=0; i<pThread->numThread; i++ )
		{
			MThreadPool::createTask( deformCompute, ( void* )&pThread[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}


void sgSlidingDeformer::endThread()
{
}


MStatus sgSlidingDeformer::computeSliding()
{
	MStatus status;

	setThread();
	MThreadPool::newParallelRegion( parallelCompute, m_pThread );
	endThread();

	return MS::kSuccess;
}