#ifndef _inverseSkinCluster_def_h
#define _inverseSkinCluster_def_h

#include "inverseSkinCluster.h"

MStatus inverseSkinCluster::updateWeightList()
{
	MStatus status;

	MFnDependencyNode thisNode = thisMObject();
	MPlug targetSkinPlug = thisNode.findPlug( aTargetSkinCluster );

	MPlugArray connections;
	targetSkinPlug.connectedTo( connections, true, false );

	if( connections.length() == 0 )
		return MS::kFailure;

	MFnDependencyNode skinNode = connections[0].node();

	MPlug weightListPlug = skinNode.findPlug( "weightList" );

	int weightListPlugNumElements = weightListPlug.numElements();
	int weightListPlugLastElementNum = weightListPlug[ weightListPlugNumElements -1 ].logicalIndex() + 1;

	pSkinInfo->weightsArray.resize( weightListPlugLastElementNum );
	pSkinInfo->wIndicesArray.resize( weightListPlugLastElementNum );

	for( int i=0; i<weightListPlugNumElements; i++ )
	{
		MPlug weightsPlug = weightListPlug[i].child( 0 );

		int weightsPlugNumElements = weightsPlug.numElements();
		pSkinInfo->weightsArray[i].setLength( weightsPlugNumElements );
		pSkinInfo->wIndicesArray[i].setLength( weightsPlugNumElements );

		for( int j=0; j< weightsPlugNumElements; j++ )
		{
			pSkinInfo->weightsArray[i][j] = weightsPlug[j].asFloat();
			pSkinInfo->wIndicesArray[i][j] = weightsPlug[j].logicalIndex();
		}
	}
	return MS::kSuccess;
}

MStatus inverseSkinCluster::updateLogicalIndexArray()
{
	MFnDependencyNode thisNode = thisMObject();
	MPlug targetSkinPlug = thisNode.findPlug( aTargetSkinCluster );

	MPlugArray connections;
	targetSkinPlug.connectedTo( connections, true, false );

	if( connections.length() == 0 )
		return MS::kFailure;

	MFnDependencyNode skinNode = connections[0].node();

	MPlug matrixPlug = skinNode.findPlug( "matrix" );

	int loofNum = matrixPlug.numElements();

	pSkinInfo->matrices.setLength( loofNum );
	pSkinInfo->bindPreMatrices.setLength( loofNum );

	MArrayDataBuilder bMatrix( aMatrix, loofNum );
	MArrayDataBuilder bBindPre( aBindPreMatrix, loofNum );

	int largeIndex = 0;
	for( int i=0; i<loofNum; i++ )
	{
		int logicalIndex = matrixPlug[i].logicalIndex();
		
		if( logicalIndex > largeIndex )
			largeIndex = logicalIndex;
	}
	logicalIndexArray.setLength( largeIndex+1 );

	for( int i=0; i<loofNum; i++ )
	{
		int logicalIndex = matrixPlug[i].logicalIndex();
		logicalIndexArray[logicalIndex] = i;
	}

	return MS::kSuccess;
}


MStatus inverseSkinCluster::updateMatrixAttribute( MArrayDataHandle& hArrMatrix, MArrayDataHandle& hArrBindPreMatrix )
{
	MFnDependencyNode thisNode = thisMObject();
	MPlug targetSkinPlug = thisNode.findPlug( aTargetSkinCluster );

	MPlugArray connections;
	targetSkinPlug.connectedTo( connections, true, false );

	if( connections.length() == 0 )
		return MS::kFailure;

	MFnDependencyNode skinNode = connections[0].node();

	MPlug matrixPlug  = skinNode.findPlug( "matrix" );
	MPlug bindPrePlug = skinNode.findPlug( "bindPreMatrix" );

	int loofNum = matrixPlug.numElements();

	if( matrixAttrUpdated && loofNum == hArrMatrix.elementCount() )
		return MS::kSuccess;

	int lastLogicalIndex = matrixPlug[ loofNum-1 ].logicalIndex();
	pSkinInfo->matrices.setLength( loofNum );
	pSkinInfo->bindPreMatrices.setLength( loofNum );

	MArrayDataBuilder bMatrix( aMatrix, loofNum );
	MArrayDataBuilder bBindPre( aBindPreMatrix, loofNum );

	for( int i=0; i<loofNum; i++ )
	{
		int logicalIndex = matrixPlug[i].logicalIndex();
		MFnMatrixData matrixPlugData  = matrixPlug[i].asMObject();
		MFnMatrixData bindPrePlugData = bindPrePlug[ logicalIndex ].asMObject();
		
		MDataHandle hMatrix  = bMatrix.addElement( i );
		MDataHandle hBindPre = bBindPre.addElement( i );

		hMatrix.set( matrixPlugData.matrix() );
		hBindPre.set( bindPrePlugData.matrix() );
	}

	int matrixElementCheck = bMatrix.elementCount();
	int bindPreElementCheck = bBindPre.elementCount();

	for( int i=loofNum; i < matrixElementCheck; i++ )
		bMatrix.removeElement( i );
	for( int i=loofNum; i < bindPreElementCheck; i++ )
		bBindPre.removeElement( i );

	hArrMatrix.set( bMatrix );
	hArrMatrix.setAllClean();

	hArrBindPreMatrix.set( bBindPre );
	hArrBindPreMatrix.setAllClean();

	matrixAttrUpdated = true;

	return MS::kSuccess;
}


MStatus inverseSkinCluster::updateMatrixInfo( MArrayDataHandle& hArrMatrix, MArrayDataHandle& hArrBindPreMatrix )
{
	int count = hArrMatrix.elementCount();
	
	hArrMatrix.jumpToElement( 0 );
	hArrBindPreMatrix.jumpToElement( 0 );

	pSkinInfo->matrices.setLength( count );
	pSkinInfo->bindPreMatrices.setLength( count );

	for( int i=0; i< count; i++ )
	{
		MDataHandle hMatrix = hArrMatrix.inputValue();
		MDataHandle hBindPre = hArrBindPreMatrix.inputValue();

		pSkinInfo->matrices[i] = hMatrix.asMatrix();
		pSkinInfo->bindPreMatrices[i] = hBindPre.asMatrix();

		hArrMatrix.next();
		hArrBindPreMatrix.next();
	}

	return MS::kSuccess;
}



void inverseSkinCluster::getWeightedMatrices( MMatrix& geomMatrix )
{
	MMatrix geomMatrixInv = geomMatrix.inverse();
	
	int matrixLength = pSkinInfo->matrices.length();

	MMatrixArray& bindPres = pSkinInfo->bindPreMatrices;
	MMatrixArray& matrices = pSkinInfo->matrices;

	MMatrixArray& multMatrixArray = pSkinInfo->multMatrices;
	multMatrixArray.setLength( matrixLength );

	for( int i=0; i< matrixLength; i++ )
		multMatrixArray[i] = geomMatrix * bindPres[i] * matrices[i] * geomMatrixInv;

	MMatrixArray& weightedMatrices = pTaskData->weightedMatrices;

	int pointLength = pTaskData->beforePoints.length();
	weightedMatrices.setLength( pointLength );

	for( int i=0; i< pointLength; i++ )
	{
		MFloatArray& weights  = pSkinInfo->weightsArray[i];
		MIntArray&   wIndices = pSkinInfo->wIndicesArray[i];

		for( int j=0; j < weights.length(); j++ )
		{
			if( multMatrixArray.length() <= logicalIndexArray[wIndices[j]] )
			{
				continue;
			}
			if( j==0 )
				weightedMatrices[i] = multMatrixArray[logicalIndexArray[wIndices[j]]] * weights[j];
			else
				weightedMatrices[i] += multMatrixArray[logicalIndexArray[wIndices[j]]] * weights[j];
		}
		weightedMatrices[i] = weightedMatrices[i].inverse();
	}
}


MStatus inverseSkinCluster::setThread()
{
	int numThread = NUM_THREAD;

	int meshPointLength = pTaskData->beforePoints.length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;

	pThread = new threadData0[ numThread ];

	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			pThread[i].start = start;
			pThread[i].end   = start+eachLength+1;
		}
		else
		{
			pThread[i].start = start;
			pThread[i].end   = start+eachLength;
		}
		pThread[i].numThread = numThread;
		pThread[i].pTaskData = pTaskData;
		pThread[i].pSkinInfo = pSkinInfo;
		start = pThread[i].end;
	}
	return MS::kSuccess;
}


MStatus inverseSkinCluster::endThread()
{
	delete []pThread;
	return MS::kSuccess;
}


void inverseSkinCluster::parallelCompute( void* data, MThreadRootTask *pRoot )
{
	threadData0* pThreadData = ( threadData0* )data;

	if( pThreadData )
	{
		for( int i=0; i< pThreadData->numThread; i++ )
		{
			MThreadPool::createTask( deformCompute, ( void* )&pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}


MThreadRetVal  inverseSkinCluster::deformCompute( void* pThread )
{
	threadData0* pThreadEach = ( threadData0* )pThread;
	taskData0*   pTaskData     = pThreadEach->pTaskData;
	skinClusterInfo* pSkinInfo = pThreadEach->pSkinInfo;

	MMatrixArray& weightedMatrices = pTaskData->weightedMatrices;
	MMatrixArray& multMatrices = pSkinInfo->multMatrices;

	for( int i= pThreadEach->start; i<pThreadEach->end ; i++ )
	{
		pTaskData->afterPoints[i] = pTaskData->beforePoints[i]*weightedMatrices[i];
		pTaskData->envPoints[i]   = pTaskData->afterPoints[i]*pTaskData->envelop + pTaskData->basePoints[i]*pTaskData->invEnv;
	}

	return (MThreadRetVal)0;
}

#endif