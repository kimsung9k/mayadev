#include "collideMatrix.h"

MStatus  collideMatrix::getResult( MMatrixArray& mtxArrCollide, const MFloatArray valuesCollide )
{
	MStatus stauts;

	int mtxLength = mtxArrCollide.length();
	MMatrix& endMatrix = mtxArrCollide[ mtxLength-1 ];

	for( int i=0; i<mtxLength-1; i++ )
	{

	}

	return MS::kSuccess;
}