#ifndef _fixCurvesPointOnMesh_threadDef_h
#define _fixCurvesPointOnMesh_threadDef_h

#include "fixCurvesPointOnMesh.h"

MPointArray getBlendPoints( float startPosition, float blendArea, MPointArray& fromThisPoints, MPointArray& toThisPoints, MMatrix& matrix )
{
	int length = toThisPoints.length();

	MPointArray returnPoints;
	returnPoints.setLength( length );

	for( int i=0; i< length; i++ )
	{
		float indexPosition = i - startPosition;

		float resultRate;
		if( indexPosition < 0 )
			resultRate = 0;
		else if( i - startPosition - blendArea > 0 )
			resultRate = 1;
		else
		{
			float indexRate = indexPosition/blendArea;
			if( indexRate > 0.5 )
			{
				float cuRate = (indexRate - 0.5)*2;
				resultRate = ( 1 - pow( 1-cuRate,2 ) )*0.5 + 0.5;
			}
			else
			{
				float cuRate = indexRate*2;
				resultRate = pow( cuRate, 2 )*0.5;
			}
		}

		returnPoints[i] = fromThisPoints[i]*( 1-resultRate ) + toThisPoints[i]*resultRate;
		returnPoints[i] *= matrix;
	}

	return returnPoints;
}


MDoubleArray buildKnots( int numCVs, int degree )
{
	int pointLength = numCVs+degree-1;
	MDoubleArray knots;
	knots.setLength( pointLength );
	
	double maxKnot = numCVs - degree;

	double knot;
	for( int i = 0; i< knots.length(); i++ )
	{
		knot = i - degree + 1;
		
		if( knot <= 0 )
			knot = 0;
		else if( knot >= maxKnot )
			knot = maxKnot;

		knots[i] = knot;
	}
	return knots;
}


MMatrix   getMatrixByVtxPoints( MPointArray vtxPoints )
{
	MPoint yPoint = vtxPoints[0];
	MPoint cPoint = vtxPoints[1];
	MPoint xPoint = vtxPoints[2];

	MVector yVector = yPoint - cPoint;
	MVector xVector = xPoint - cPoint;
	
	double avDist = ( yVector.length() + xVector.length() )/ 2.0;

	MVector zVector = ( xVector^yVector ).normal() * avDist;

	double buildMatrix[4][4] = { xVector.x, xVector.y, xVector.z, 0,
		                         yVector.x, yVector.y, yVector.z, 0,
						         zVector.x, zVector.y, zVector.z, 0,
						         cPoint.x , cPoint.y,  cPoint.z,  1 };

	return MMatrix( buildMatrix );
}


threadData*  fixCurvesPointOnMesh::createThread( taskData* pTask, int threadNum )
{
	threadData* pThread = new threadData[ threadNum ];

	int allLength = pTask->length;

	int eachLength = allLength / threadNum;

	int diff = allLength - eachLength * threadNum;

	int cuLength = eachLength;
	if( diff )
		cuLength++;

	for( int i=0; i< threadNum; i++ )
	{
		pThread[i].startNum = i * cuLength;
		pThread[i].endNum   = ( i+1 ) * cuLength - 1;
		pThread[i].pTask    = pTask;
		pThread[i].numThread = threadNum;

		if( pThread[i].endNum >= allLength )
			pThread[i].endNum = allLength -1;
		if( i >= allLength )
			pThread[i].endNum = -1;

		//cout << " i : " << i << endl;
		//cout << "allLength   : " << allLength   << endl;

		//printf( "startNum : %d,  endNum : %d\n", pThread[i].startNum, pThread[i].endNum );
	}

	return pThread;
}


void fixCurvesPointOnMesh::parallelCompute( void* pData, MThreadRootTask* pRoot )
{
	threadData* pThreadData = ( threadData* )pData;
	
	int numThread = pThreadData->numThread;

	if( pThreadData )
	{
		for( int i=0; i< numThread; i++ )
		{
			MThreadPool::createTask( threadCompute, ( void* )&pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}


MThreadRetVal fixCurvesPointOnMesh::threadCompute( void *pData )
{
	threadData* pThreadData = ( threadData* )pData;
	
	int threadNum = pThreadData->numThread;
	taskData* taskPtr = pThreadData->pTask;

	int numSample = taskPtr->length;
	float startPosition = taskPtr->startPosition;
	float blendArea     = taskPtr->blendArea;
	
	MPointArray blendPoints;

	printf( "thread compute -- start : %d, %d \n", pThreadData->startNum, pThreadData->endNum);

	for( int i=pThreadData->startNum; i<= pThreadData->endNum; i++ )
	{
		MPointArray& startCurvePoints = taskPtr->pStartCurvePoints[i];
		MPointArray& movedCurvePoints = taskPtr->pMovedCurvePoints[i];
		MMatrix      moveMatrix       = getMatrixByVtxPoints( taskPtr->pVtxPoints[i] );

		int curvePointLength = movedCurvePoints.length();

		MPointArray  multMatrixMovePoints;
		multMatrixMovePoints.setLength( curvePointLength );
		for( int j=0; j<curvePointLength; j++ )
		{
			multMatrixMovePoints[j] = movedCurvePoints[j]*moveMatrix.inverse();
		}
		taskPtr->pKnots[i] = buildKnots( startCurvePoints.length(), taskPtr->pDegrees[i] );
		taskPtr->pCurrentCurvePoints[i] = getBlendPoints( startPosition, blendArea, startCurvePoints, multMatrixMovePoints, moveMatrix );
	}
	return 0;
}

#endif