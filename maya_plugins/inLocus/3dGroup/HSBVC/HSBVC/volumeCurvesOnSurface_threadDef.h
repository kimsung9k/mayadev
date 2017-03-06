#ifndef _volumeCurvesOnSurface_threadDef_h
#define _volumeCurvesOnSurface_threadDef_h

#include "volumeCurvesOnSurface.h"

pointThreadData*  volumeCurvesOnSurface::createPointThread( pointTaskData* pointTaskPtr, int allPointNum, int numThread )
{
	pointThreadData* pointThread = new pointThreadData[ numThread ];

	int eachLength = allPointNum / numThread;

	int diff = allPointNum - eachLength * numThread;

	int cuLength;
	for( int i=0; i< numThread; i++ )
	{
		if( diff )
		{
			cuLength = eachLength +1;
			diff--;
		}
		else
			cuLength = eachLength;

		pointThread[i].startNum = i * cuLength;
		pointThread[i].endNum   = ( i+1 ) * cuLength - 1;
		pointThread[i].numThread = numThread;
		pointThread[i].threadNum = i;
		pointThread[i].pointTaskPtr = pointTaskPtr;
	}

	return pointThread;
}


void volumeCurvesOnSurface::parallelCompute( void* pData, MThreadRootTask* pRoot )
{
	pointThreadData* pThreadData = ( pointThreadData* )pData;
	
	int numThread = pThreadData->numThread;

	if( pThreadData )
	{
		for( int i=0; i< numThread; i++ )
		{
			MThreadPool::createTask( threadCompute, ( void* )& pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}

MThreadRetVal volumeCurvesOnSurface::threadCompute( void *pData )
{
	pointThreadData* pThreadData = ( pointThreadData* )pData;
	
	int numThread = pThreadData->numThread;
	pointTaskData* taskPtr = pThreadData->pointTaskPtr;

	MFnNurbsSurface* fnSurface = taskPtr->pFnSurface[ pThreadData->threadNum ];
	MFnNurbsCurve*   fnCurve   = taskPtr->pFnCurve[ pThreadData->threadNum ];

	int numSample = taskPtr->paramUArr.length();

	int uIndex;
	int vIndex;
	double centerParamValue;
	double uParamValue;
	double vParamValue;
	double centerRate;

	MPoint surfPoint;
	MPoint crvPoint;

	MPointArray& points = taskPtr->allPointArr;
	for( int i=pThreadData->startNum; i<= pThreadData->endNum; i++ )
	{
		uIndex = i % numSample;
		vIndex = i / numSample;
		
		centerParamValue = taskPtr->centerParamArr[ uIndex ];
		uParamValue = taskPtr->paramUArr[ uIndex ];
		vParamValue = taskPtr->paramVArr[ vIndex ];
		centerRate  = taskPtr->centerRateArr[ vIndex ];
		
		fnSurface->getPointAtParam( uParamValue, vParamValue, surfPoint );
		fnCurve  ->getPointAtParam( centerParamValue, crvPoint );
		points[i] = crvPoint * (1-centerRate) + surfPoint * centerRate;
		points[i]*= taskPtr->matrix;
	}
	return 0;
}

#endif