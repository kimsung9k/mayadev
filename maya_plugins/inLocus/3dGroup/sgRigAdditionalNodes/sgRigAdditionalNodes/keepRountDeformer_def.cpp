#include "keepRoundDeformer.h"

MStatus keepRoundDeformer::editPointsWidthMatrix( const MDoubleArray& distsPoint,const MPointArray& editPointArr,
		                           MPointArray& outPointArr, MMatrix& matrix, float envValue )
{
	MStatus status;

	MMatrix invMatrix = matrix.inverse();

	int lengthPoints = distsPoint.length();
	outPointArr.setLength( lengthPoints );

	float multDist;
	float invEnv = 1.0f - envValue;
	for( int i=0; i< lengthPoints; i++ )
	{
		MVector editPoint = editPointArr[i] * invMatrix;
		multDist = distsPoint[i] / editPoint.length();

		multDist = invEnv + multDist * envValue;

		outPointArr[i] = editPoint * multDist;
		outPointArr[i] *= matrix;
	}

	return MS::kSuccess;
}