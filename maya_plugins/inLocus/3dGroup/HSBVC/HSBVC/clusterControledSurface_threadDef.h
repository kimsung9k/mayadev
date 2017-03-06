#ifndef _clusterControledSurface_threadDef_h
#define _clusterControledSurface_threadDef_h

#include "clusterControledSurface.h"


ThreadData* clusterControledSurface::createThreadData( int numTasks, TaskData* pTaskData )
{
	ThreadData* pThreadData = new ThreadData[ numTasks ];
	pThreadData->pTaskData = pTaskData;

	int pointLength = pTaskData->points.length();
	int divLength = pointLength / numTasks;
	int restLength = pointLength - numTasks*divLength;

	int eachLength;

	int start = 0;
	for( int i=0; i<numTasks; i++ )
	{
		if( restLength > 0 )
			eachLength = divLength + 1;
		else
			eachLength = divLength;

		pThreadData[i].start = start;
		pThreadData[i].end   = start + eachLength;
		pThreadData[i].numTasks = numTasks;

		//printf( "thread[%d] - start : %d, end : %d\n", i, pThreadData[i].start, pThreadData[i].end );

		start += eachLength;
		restLength--;
	}
	cout << pointLength << endl;

	return pThreadData;
}


void  clusterControledSurface::createTasks( void* pData, MThreadRootTask *pRoot )
{
	ThreadData* pThreadData = ( ThreadData* )pData;

	cout << "createTasks" << endl;

	if( pThreadData )
	{
		int numTasks = pThreadData->numTasks;
		for( int i=0; i < numTasks; i++ )
		{
			MThreadPool::createTask( threadCaculate, ( void* )&pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}

MThreadRetVal  clusterControledSurface::threadCaculate( void* pParam )
{
	ThreadData* pThreadData = ( ThreadData* )pParam;
	TaskData* pTaskData = pThreadData->pTaskData;

	MPointArray& points = pTaskData->points;
	MDoubleArray& paramPerPoints = pTaskData->paramPerPoints;
	MDoubleArray& paramPerMatrix = pTaskData->paramPerMatrix;

	int start = pThreadData->start;
	int end   = pThreadData->end;
	for( int i= start; i<end; i++ )
	{
		printf( "point index : %d, pointLength : %d\n", i, points.length() );
	}
	return 0;
}

#endif