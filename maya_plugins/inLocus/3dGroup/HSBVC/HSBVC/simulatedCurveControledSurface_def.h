#include "simulatedCurveControledSurface.h"

void getMatrixArrayFromCurve( MMatrix& upMatrix, MFnNurbsCurve& fnCurve, 
	                          MMatrixArray& returnMtxArr,
							  int upMatrixNum = 0 )
{
	if( !upMatrixNum )
		upMatrixNum  = fnCurve.numSpans();

	double maxParam = fnCurve.findParamFromLength( fnCurve.length() );
	double minParam = fnCurve.findParamFromLength( 0 );
	double rangeDistance = maxParam - minParam;

	double eachRange = ( maxParam - minParam ) / (upMatrixNum-1);

	returnMtxArr.setLength( upMatrixNum );

	MPoint  pivPoint;
	MVector aimVector;
	double searchParam;
	MMatrix returnMatrix;

	for( int i=0; i<upMatrixNum; i++ )
	{
		searchParam = eachRange*i+minParam;

		fnCurve.getPointAtParam( searchParam, pivPoint );
		aimVector = fnCurve.tangent( searchParam );
		aimVector*= upMatrix.inverse();

		aimVector.normalize();

		MVector upVector( -aimVector.y, aimVector.x, 0 );
		MVector otherVector( -aimVector.z, 0, aimVector.x );

		MVector editUpVector = otherVector^aimVector;

		double absY = abs( aimVector.y );

		upVector = upVector*absY + editUpVector*( 1-absY ); 

		otherVector = aimVector^upVector;
		upVector = otherVector^aimVector;

		otherVector.normalize();
		upVector.normalize();

		double buildMatrix[4][4] = { aimVector.x, aimVector.y, aimVector.z, 0,
									 upVector.x,  upVector.y,  upVector.z, 0,
									 otherVector.x, otherVector.y, otherVector.z, 0,
									 0, 0, 0, 1.0 };

		returnMatrix = MMatrix( buildMatrix )*upMatrix;
		upMatrix = returnMatrix;

		returnMatrix(3,0) = pivPoint.x;
		returnMatrix(3,1) = pivPoint.y;
		returnMatrix(3,2) = pivPoint.z;

		returnMtxArr[i] = returnMatrix;
	}
}


MThreadRetVal  simulatedCurveControledSurface::compute_getLocalPoints( void* data )
{
	getLocalPointsThread* p_thread = ( getLocalPointsThread* ) data;

	getLocalPointsTask* p_task = p_thread->p_task;

	MPointArray&  surfacePoints = *(p_task->p_surfaceWorldPoints);
	MPointArray&  surfacePivPoints = *(p_task->p_surfacePivPoints);
	MMatrixArray& upMatrixArr   = *(p_task->p_upMatrixArr);
	MIntArray&    paramIndies   = *(p_task->p_paramIndies);
	MFloatArray&  paramWeights  = *(p_task->p_paramWeights);

	MPointArray&  returnPoints = *(p_task->p_returnPoints);

	int upMatrixLength = upMatrixArr.length();

	int paramIndex;
	float paramWeight;
	MMatrix weightedMatrix;
	for( int i=p_thread->start; i<p_thread->end; i++ )
	{
		paramIndex = paramIndies[i];
		paramWeight = paramWeights[i];

		if( paramIndex == upMatrixLength-1 )
		{
			weightedMatrix = upMatrixArr[paramIndex];
		}
		else
		{
			weightedMatrix = ( upMatrixArr[paramIndex]*(1-paramWeight)+upMatrixArr[paramIndex+1]*paramWeight );
		}
		weightedMatrix(3,0) = surfacePivPoints[i].x;
		weightedMatrix(3,1) = surfacePivPoints[i].y;
		weightedMatrix(3,2) = surfacePivPoints[i].z;

		returnPoints[i] = surfacePoints[i]*weightedMatrix.inverse();
	}

	return (MThreadRetVal)0;
}



void  simulatedCurveControledSurface::parallel_getLocalPoints( void* data, MThreadRootTask* root )
{
	getLocalPointsThread* p_thread = ( getLocalPointsThread* ) data;

	for( int i=0; i< p_thread->numThread; i++ )
	{
		getLocalPointsThread& thread = p_thread[i];
		MThreadPool::createTask( compute_getLocalPoints, (void*)&thread, root );
	}
	MThreadPool::executeAndJoin( root );
}



void simulatedCurveControledSurface::getLocalPointsFromSurface( 
	                            MFnNurbsSurface& fnSurface, MMatrix& baseSurfaceMatrix,
	                            MFnNurbsCurve& fnCurve, 
	                            MMatrixArray& upMatrixArr,
								MPointArray& returnPointArr,
								MDoubleArray& returnParamArr )
{
	int upMatrixNum = upMatrixArr.length();

	MPointArray surfCVs;
	fnSurface.getCVs( surfCVs );
	int surfPointLength = surfCVs.length();

	double minParam = fnCurve.findParamFromLength( 0 );
	double maxParam = fnCurve.findParamFromLength( fnCurve.length() );
	double paramLength = maxParam - minParam;
	double eachRange = paramLength/( upMatrixNum - 1 );

	MPoint surfPoint;
	MPointArray closePoints;
	closePoints.setLength( surfPointLength );
	double param;

	MIntArray    paramIndies;
	MFloatArray  paramWeights;

	paramIndies.setLength( surfPointLength );
	paramWeights.setLength( surfPointLength );
	returnPointArr.setLength( surfPointLength );
	returnParamArr.setLength( surfPointLength );

	for( int i=0; i<surfPointLength ; i++ )
	{
		surfCVs[i]*=baseSurfaceMatrix;
		closePoints[i] = fnCurve.closestPoint( surfCVs[i], &param, 0.1 );

		float currentRange = ( param - minParam )/eachRange;
		returnParamArr[i] = ( param - minParam )/paramLength;
		paramIndies[i]  = currentRange;
		paramWeights[i] = currentRange - paramIndies[i];
	}

	int numThread = NUM_THREAD;

	getLocalPointsTask task;

	task.p_surfaceWorldPoints = &surfCVs;
	task.p_surfacePivPoints = &closePoints;
	task.p_upMatrixArr    = &upMatrixArr;
	task.p_paramIndies  = &paramIndies;
	task.p_paramWeights = &paramWeights;
	task.p_returnPoints = &returnPointArr;
	task.p_paramRanges  = &returnParamArr;

	getLocalPointsThread* thread = new getLocalPointsThread[ numThread ];

	int eachLength = surfPointLength/numThread;
	int restLength = surfPointLength - eachLength*numThread;

	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if( restLength-- > 0 )
		{
			thread[i].start = start;
			thread[i].end   = start+eachLength+1;
		}
		else
		{
			thread[i].start = start;
			thread[i].end   = start+eachLength;
		}
		thread[i].numThread = numThread;
		thread[i].p_task = &task;

		start = thread[i].end;
	}

	MThreadPool::init();
	MThreadPool::newParallelRegion( parallel_getLocalPoints, thread );
	MThreadPool::release();
	
	delete[] thread;/**/
}


MThreadRetVal simulatedCurveControledSurface::compute_getResultPoints( void* data )
{
	getResultPointsThread* p_thread = ( getResultPointsThread* ) data;

	getResultPointsTask* p_task = p_thread->p_task;
	MMatrix&    surfaceMatrix  = *(p_task->p_surfaceMatrix);
	MPointArray&  localPoints  = *(p_task->p_localPoints);
	MPointArray&  localPivots  = *(p_task->p_localPivots);
	MMatrixArray& upMatrixList = *(p_task->p_upMatrixList);
	MDoubleArray& paramList    = *(p_task->p_paramList);
	MPointArray&  returnPoints = *(p_task->p_returnPoints);

	int upMatrixLength = upMatrixList.length();

	double minParam = p_thread->minParam;
	double maxParam = p_thread->maxParam;
	double paramLength = maxParam - minParam;
	double eachLength = paramLength / (upMatrixLength-1);

	double param;
	double paramRate;

	int minIndex;
	int maxIndex;

	float weight;

	MMatrix weightedMatrix;

	MVector aimVector;
	MVector upVector;
	MVector byNormal;

	MMatrix resultMatrix;
	MMatrix surfaceMatrixInverse = surfaceMatrix.inverse();

	for( int i=p_thread->start; i<p_thread->end; i++ )
	{
		param = paramList[i];

		paramRate = (param - minParam)/eachLength;
		minIndex = paramRate;
		if( minIndex == upMatrixLength-1 )
			maxIndex = minIndex;
		else
			maxIndex = minIndex + 1;

		weight = (paramRate - minIndex);

		weightedMatrix = upMatrixList[ minIndex ]*( 1.0f-weight ) + upMatrixList[ maxIndex ]*weight;

		aimVector = MVector( weightedMatrix(0,0), weightedMatrix(0,1), weightedMatrix(0,2) );
		upVector  = MVector( weightedMatrix(1,0), weightedMatrix(1,1), weightedMatrix(1,2) );
		byNormal  = MVector( weightedMatrix(2,0), weightedMatrix(2,1), weightedMatrix(2,2) );

		double buildMatrix[4][4] = { aimVector.x, aimVector.y, aimVector.z, 0,
			                         upVector.x,  upVector.y,  upVector.z,  0,
									 byNormal.x,  byNormal.y,  byNormal.z,  0,
									 localPivots[i].x, localPivots[i].y, localPivots[i].z, 1 };

		resultMatrix = MMatrix( buildMatrix );

		returnPoints[i] = localPoints[i]*resultMatrix*surfaceMatrixInverse;
	}
	return (MThreadRetVal)0;
}

void simulatedCurveControledSurface::parallel_getResultPoints( void* data, MThreadRootTask* root )
{
	getResultPointsThread* p_thread = ( getResultPointsThread* ) data;

	for( int i=0; i< p_thread->numThread; i++ )
	{
		getResultPointsThread& thread = p_thread[i];
		MThreadPool::createTask( compute_getResultPoints, (void*)&thread, root );
	}
	MThreadPool::executeAndJoin( root );
}

void simulatedCurveControledSurface::getSurfaceMovePoints( MMatrix& baseSurfaceMatrix,
	                       MPointArray& localPoints,  MPointArray& localPivs,
						   MDoubleArray& paramList,
						   MMatrixArray& upMatrixList,
						   double minParam, double maxParam,
						   MPointArray& returnPoints )
{
	int numThread = NUM_THREAD;

	int surfPointLength = localPoints.length();
	int eachLength = surfPointLength/numThread;
	int restLength = surfPointLength - eachLength*numThread;

	returnPoints.setLength( surfPointLength );

	getResultPointsTask task;
	
	task.p_surfaceMatrix = &baseSurfaceMatrix;
	task.p_localPoints  = &localPoints;
	task.p_localPivots  = &localPivs;
	task.p_upMatrixList = &upMatrixList;
	task.p_paramList    = &paramList;
	task.p_returnPoints = &returnPoints;

	getResultPointsThread* thread = new getResultPointsThread[ numThread ];

	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if( restLength-- > 0 )
		{
			thread[i].start = start;
			thread[i].end   = start+eachLength+1;
		}
		else
		{
			thread[i].start = start;
			thread[i].end   = start+eachLength;
		}
		thread[i].numThread = numThread;
		thread[i].minParam = minParam;
		thread[i].maxParam = maxParam;
		thread[i].p_task = &task;
		start = thread[i].end;
	}
	MThreadPool::init();
	MThreadPool::newParallelRegion( parallel_getResultPoints, thread );
	MThreadPool::release();

	delete []thread;
}


MStatus  simulatedCurveControledSurface::setDependentsDirty( const MPlug &plug,  MPlugArray  &plugArray )
{
	if ( plug.partialName() == "baseSurface" )
	{
	   	requireUpdateSurface = true;
    }
	else if ( plug.partialName() == "baseSurfaceMatrix" )
	{
	   	requireUpdateSurface = true;
    }
	else if( plug.partialName() == "baseUpMatrix" )
	{
		requireUpdateSurface = true;
		requireUpdateCurve = true;
	}
	else if( plug.partialName() == "baseCurve" )
	{
		requireUpdateCurve = true;
	}
    return( MS::kSuccess );
}