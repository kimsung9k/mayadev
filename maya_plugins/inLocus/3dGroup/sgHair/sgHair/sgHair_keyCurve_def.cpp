#include "sgHair_keyCurve.h"


MStatus getMtxMultPoints( MPointArray& targetPoints, const MMatrix& mtxBase, const MPointArray& points )
{
	MStatus status;

	int lengthPoints = points.length();
	targetPoints.setLength( lengthPoints );

	for( int i=0; i< lengthPoints; i++ )
	{
		targetPoints[i] = points[i] * mtxBase;
	}

	return MS::kSuccess;
}



MPointArray getBlendPoints( const MPointArray& pointsFirst, const MPointArray& pointsSecond, float weight )
{
	MPointArray pointsOutput;

	pointsOutput.setLength( pointsFirst.length() );

	float invWeight = 1.0f - weight;

	for( int i=0; i< pointsOutput.length(); i++ )
	{
		pointsOutput[i] = pointsFirst[i] * invWeight + pointsSecond[i] * weight;
	}

	return pointsOutput;
}



MPointArray getDiffPoints( const MPointArray& pointsFirst, const MPointArray& pointsSecond )
{
	MPointArray pointsOutput;

	int length = pointsFirst.length();
	pointsOutput.setLength( length );

	for( int i=0; i< length; i++ )
	{
		pointsOutput[i] = pointsFirst[i] - pointsSecond[i];
	}
	return pointsOutput;
}


MPointArray getSumPoints( const MPointArray& pointsFirst, const MPointArray& pointsSecond )
{
	MPointArray pointsOutput;

	int length = pointsFirst.length();
	pointsOutput.setLength( length );

	for( int i=0; i< length; i++ )
	{
		pointsOutput[i] = pointsFirst[i] + pointsSecond[i];
	}
	return pointsOutput;
}


MPointArray getWeightedPoints( const MPointArray& points, float weight )
{
	MPointArray pointsOutput;
	int length = points.length();
	pointsOutput.setLength( length );

	for( int i=0; i< length; i++ )
	{
		pointsOutput[i] = points[i] * weight;
	}
	return pointsOutput;
}


MStatus sgHair_keyCurve::getOutputPoints( const MPointArray& inputPoints, MPointArray& outputPoints, 
	const MMatrix& mtxBase,
	const MTime& time, const sgHair_keyCurve_keys& keys,
	const MTimeArray& timesSorted, const MIntArray& indicesSorted,
	float envValue )
{
	MStatus status;

	int firstIndex = -1;
	int secondIndex = -1;

	for( unsigned int i=0; i< timesSorted.length(); i++ )
	{
		secondIndex = i;
		if( time >= timesSorted[i] )
		{
			firstIndex = i;
			continue;
		}
		if( time < timesSorted[i] )
		{
			if( firstIndex == -1 ) continue;
			break;
		}
	}

	if( firstIndex == -1 && secondIndex == -1 )
	return MS::kSuccess;

	if( firstIndex == -1 || secondIndex == -1 ) 
	{
		firstIndex = 0;
		secondIndex = 0;
	}

	MTime timeFirst = timesSorted[ firstIndex ];
	MTime timeSecond = timesSorted[ secondIndex ];

	float weight= 1.0;

	float div = timeSecond.value() - timeFirst.value();
	if( div != 0 )
	{
		weight = ( time.value() - timeFirst.value() )/ div;
	}

	MMatrix& mtxBaseFirst  = keys.getMatrix( indicesSorted[ firstIndex ] );
	MMatrix& mtxBaseSecond = keys.getMatrix( indicesSorted[ secondIndex ] );
	MPointArray& pointsFirstWorld = keys.getPoints( indicesSorted[ firstIndex ] );
	MPointArray& pointsSecondWorld = keys.getPoints( indicesSorted[ secondIndex ] );

	MPointArray pointsLocalInput;
	getMtxMultPoints( pointsLocalInput, mtxBase.inverse(),  inputPoints );

	MPointArray pointsFirstLocal;
	MPointArray pointsSecondLocal;
	MPointArray pointsFirstDiff;
	MPointArray pointsSecondDiff;

	MPointArray pointsOutput;

	getMtxMultPoints( pointsFirstLocal, mtxBaseFirst.inverse(),  pointsFirstWorld );
	getMtxMultPoints( pointsSecondLocal, mtxBaseSecond.inverse(), pointsSecondWorld );
	pointsFirstDiff  = getDiffPoints( pointsFirstLocal, pointsLocalInput );
	pointsSecondDiff = getDiffPoints( pointsSecondLocal, pointsLocalInput );

	MPointArray pointsBlend = getBlendPoints( pointsFirstDiff, pointsSecondDiff, weight );

	if( envValue==1 )
	{
		getMtxMultPoints( outputPoints, mtxBase, getSumPoints( pointsBlend, pointsLocalInput ) );
	}
	else
	{
		MPointArray envPoints = getWeightedPoints( pointsBlend, envValue );
		getMtxMultPoints( outputPoints, mtxBase, getSumPoints( envPoints, pointsLocalInput ) );
	}

	return MS::kSuccess;
}