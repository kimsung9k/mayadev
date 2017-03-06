#ifndef _blendAndFixedShape_def_h
#define _blendAndFixedShape_def_h

#include "blendAndFixedShape.h"
#include "blendAndFixedShape_weightDef.h"

MStatus    blendAndFixedShape::meshPoints_To_DeltaAttrs( MArrayDataHandle& hArrBlendMeshInfos )
{
	MStatus status;

	int blendMeshNum = hArrBlendMeshInfos.elementCount();

	if( beforeBlendMeshNum != hArrBlendMeshInfos.elementCount() )
	{
		updateBlendMeshIndices.clear();
		updateBlendMeshIndices.setLength( hArrBlendMeshInfos.elementCount() );

		for( int i=0; i< hArrBlendMeshInfos.elementCount(); i++ )
		{
			hArrBlendMeshInfos.jumpToElement( i );
			updateBlendMeshIndices[i] = hArrBlendMeshInfos.elementIndex();
		}
		beforeBlendMeshNum = hArrBlendMeshInfos.elementCount();
	}

	MFnDependencyNode fnThisNode = thisMObject();
	MPlug plugBlendMeshInfos = fnThisNode.findPlug( "blendMeshInfos" );
	MPlugArray cons;

	int index;
	for( int i=0; i< updateBlendMeshIndices.length(); i++ )
	{
		index = updateBlendMeshIndices[i];

		hArrBlendMeshInfos.jumpToElement( index );
		updateDeltaIndices.append( index );

		MDataHandle hBlendMeshInfo = hArrBlendMeshInfos.inputValue( &status );
		if( !status ) return status;

		MDataHandle      hInputMesh = hBlendMeshInfo.child( aInputMesh );
		MArrayDataHandle hArrDeltas = hBlendMeshInfo.child( aDeltas );
		MDataHandle      hMeshName  = hBlendMeshInfo.child( aMeshName );
		
		MPlug plugInputMesh = plugBlendMeshInfos[index].child( 0 );

		cons.clear();
		plugInputMesh.connectedTo( cons, true, false );
		if( !cons.length() ) continue;

		MFnMesh fnMesh = cons[0].node();
		MPointArray meshPoints;

		fnMesh.getPoints( meshPoints );

		MPoint deltaPoint;

		MIntArray deltaIndices;
		MPointArray deltas;

		for( int j=0; j < pTaskData->basePoints.length(); j++ )
		{
			deltaPoint = meshPoints[j] - pTaskData->basePoints[j];

			if( fabs( deltaPoint.x ) < 0.0001 &&
				fabs( deltaPoint.y ) < 0.0001 &&
				fabs( deltaPoint.z ) < 0.0001 )
			{
			}
			else
			{
				deltaIndices.append( j );
				deltas.append( deltaPoint );
			}
		}
		
		MArrayDataBuilder builder( aDeltas, deltaIndices.length() );
		builder.setGrowSize( deltaIndices.length() );

		for( int j=0; j < deltaIndices.length(); j++ )
		{
			MDataHandle hDelta = builder.addElement( deltaIndices[j] );
			hDelta.setMVector( deltas[j] );
		}

		int elementCheck = builder.elementCount();

		for( int j=deltaIndices.length(); j < elementCheck; j++ )
		{
			builder.removeElement( j );
		}
		hArrDeltas.set( builder );
		hArrDeltas.setAllClean();
	}

	return MS::kSuccess;
}


MStatus    blendAndFixedShape::deltaAttrs_To_Task( MArrayDataHandle& hArrBlendMeshInfos )
{
	MStatus status;

	int blendMeshNum = hArrBlendMeshInfos.elementCount();

	vector<MPointArray>& deltas       = pTaskData->deltas;

	deltas.resize( blendMeshNum );

	int index;

	hArrBlendMeshInfos.next();
	hArrBlendMeshInfos.jumpToElement( 0 );

	for( int i=0; i< updateDeltaIndices.length(); i++ )
	{
		index = updateDeltaIndices[i];

		hArrBlendMeshInfos.jumpToElement( index );
		MDataHandle hBlendMeshInfo = hArrBlendMeshInfos.inputValue( &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MArrayDataHandle hArrDeltas = hBlendMeshInfo.child( aDeltas );

		deltas[index].setLength( pTaskData->basePoints.length() );

		MVector deltaPoint;
		
		for( int j=0; j<pTaskData->basePoints.length(); j++ )
		{
			deltas[index][j] = MPoint( 0,0,0 );
		}

		hArrDeltas.jumpToElement( 0 );
		for( int j=0; j< hArrDeltas.elementCount(); j++ )
		{
			MDataHandle hDelta = hArrDeltas.inputValue();

			deltaPoint = hDelta.asVector();

			deltas[index][hArrDeltas.elementIndex()] = deltaPoint;
			hArrDeltas.next();
		}
	}
	return MS::kSuccess;
}

/*
MStatus    blendAndFixedShape::reOrdereDeltas( MArrayDataHandle& hArrBlendMeshInfos )
{
	MStatus status;

	cout << "updateBlendMeshIndices : " << updateBlendMeshIndices << endl;
	if( !updateBlendMeshIndices.length() )
		return MS::kSuccess;

	int blendMeshNum = hArrBlendMeshInfos.elementCount();

	vector<MPointArray>& deltas       = pTaskData->deltas;
	deltas.clear();
	deltas.resize( 0 );

	vector<MPointArray>::iterator delta_it = deltas.begin();
	
	int index = -1;

	MIntArray ArrBlendMeshInfosIndices;

	hArrBlendMeshInfos.next();
	MPointArray deltaPoints;
	deltaPoints.setLength( pTaskData->basePoints.length() );

	
	hArrBlendMeshInfos.next();
	for( int j=0; j< blendMeshNum; j++ )
	{	
		hArrBlendMeshInfos.jumpToElement(j);
		MDataHandle hBlendMeshInfo = hArrBlendMeshInfos.inputValue( &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MArrayDataHandle hArrDeltas = hBlendMeshInfo.child( aDeltas );

		hArrDeltas.jumpToElement( 0 );
		MVector deltaPoint;

		for( int j=0; j< deltaPoints.length(); j++ )
			deltaPoints[j] = MPoint( 0,0,0 );

		for( int j=0; j< hArrDeltas.elementCount(); j++ )
		{
			MDataHandle hDelta = hArrDeltas.inputValue();
			deltaPoints[ hArrDeltas.elementIndex() ] = hDelta.asVector();
			hArrDeltas.next();
		}

		int elementIndex = hArrBlendMeshInfos.elementIndex();
		if( ArrBlendMeshInfosIndices.length() == 0 )
		{	
			ArrBlendMeshInfosIndices.append( hArrBlendMeshInfos.elementIndex() );
			deltas.push_back( deltaPoints );
			delta_it = deltas.begin();
			continue;
		}

		bool inserted = false;
		for( int k=0; k < ArrBlendMeshInfosIndices.length(); k++ )
		{
			if( ArrBlendMeshInfosIndices[k] > elementIndex )
			{
				ArrBlendMeshInfosIndices.insert( elementIndex, k );
				delta_it = deltas.insert( delta_it+k, deltaPoints );
				delta_it -= k;
				inserted = true;
				break;
			}
		}

		if( !inserted )
		{
			ArrBlendMeshInfosIndices.append( elementIndex );
			deltas.push_back( deltaPoints );
		}
		hArrBlendMeshInfos.next();
	}
	return MS::kSuccess;
}
*/

void blendAndFixedShape::setThread()
{
	int numThread = NUM_THREAD;

	int meshPointLength = pTaskData->basePoints.length();
	int eachLength = meshPointLength/numThread;
	int restLength = meshPointLength - eachLength*numThread;

	pThreadData = new blendAndFixedShape_threadData[ numThread ];
	
	int start=0;
	for( int i=0; i< numThread; i++ )
	{
		if(  0 < restLength-- )
		{
			pThreadData[i].start = start;
			pThreadData[i].end   = start+eachLength+1;
		}
		else
		{
			pThreadData[i].start = start;
			pThreadData[i].end   = start+eachLength;
		}
		pThreadData[i].numThread = numThread;
		pThreadData[i].pTaskData = pTaskData;
		start = pThreadData[i].end;
	}
}


void blendAndFixedShape::endThread()
{
	//delete []pThreadData;
}

void blendAndFixedShape::parallelCompute( void* data, MThreadRootTask *pRoot )
{
	blendAndFixedShape_threadData* pThreadData = ( blendAndFixedShape_threadData* )data;

	if( pThreadData )
	{
		for( int i=0; i< pThreadData->numThread; i++ )
		{
			MThreadPool::createTask( deformCompute, ( void* )&pThreadData[i], pRoot );
		}
		MThreadPool::executeAndJoin( pRoot );
	}
}

MThreadRetVal  blendAndFixedShape::deformCompute( void* pThread )
{
	blendAndFixedShape_threadData* pThreadEach = ( blendAndFixedShape_threadData* )pThread;
	blendAndFixedShape_taskData*   pTaskData     = pThreadEach->pTaskData;

	MPoint addPoint;
	int weightedIndex;

	for( int i= pThreadEach->start; i<pThreadEach->end ; i++ )
	{
		addPoint.x = 0;
		addPoint.y = 0;
		addPoint.z = 0;

		for( int j=0; j<pTaskData->weightedIndices.length(); j++ )
		{
			weightedIndex = pTaskData->weightedIndices[j];
			addPoint += pTaskData->deltas[weightedIndex][i]*pTaskData->blendMeshWeights[weightedIndex];
		}
		pTaskData->movedPoints[i] = addPoint + pTaskData->basePoints[i];
	}
	return (MThreadRetVal)0;
}


void  blendAndFixedShape::setWeightedBlendIndices()
{
	MFloatArray& blendMeshWeights = pTaskData->blendMeshWeights;
	MIntArray&   weightedIndices  = pTaskData->weightedIndices;

	weightedIndices.clear();

	for( int i=0; i<blendMeshWeights.length(); i++ )
	{
		if( blendMeshWeights[i] && pTaskData->deltas[i].length() )
		{
			weightedIndices.append( i );
		}
	}
}

#endif