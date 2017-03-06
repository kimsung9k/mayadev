#include "clusterControledCurve.h"


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


bool checkIsNotSame( double& first, double& second )
{
	return (fabs( first - second ) < 0.001) ? false : true ;
}


MStatus  clusterControledCurve::updateBindPreMatrix( MObject oInputCurve,
													 MMatrix mtxInputCurve,
													 MArrayDataHandle& hArrMatrix,
													 MArrayDataHandle& hArrBindPreMatrix,
													 bool update )
{
	int numElement = hArrBindPreMatrix.elementCount();


	delete []bindPreMatrix;
	bindPreMatrix = new MMatrix[ numElement ];

	for( int i=0; i<numElement ; i++ )
	{
		hArrBindPreMatrix.jumpToElement( i );
		MDataHandle hBindPreMatrix = hArrBindPreMatrix.inputValue();
		bindPreMatrix[i] = hBindPreMatrix.asMatrix();
	}
	updatePointWeights( oInputCurve, mtxInputCurve,
						hArrMatrix, hArrBindPreMatrix );

	return MS::kSuccess;
}

MStatus  clusterControledCurve::updatePointWeights( MObject oInputCurve, 
	                                                MMatrix mtxInputCurve,
													MArrayDataHandle& hArrMatrix,
													MArrayDataHandle& hArrBindPreMatrix )
{
	MStatus status;

	MFnNurbsCurve fnCurve( oInputCurve );
	int numCVs = fnCurve.numCVs();
	int numMatrix = hArrBindPreMatrix.elementCount();

	MDoubleArray matrixNearParamList;
	matrixNearParamList.setLength( numMatrix );
	MDoubleArray cvNearParamList;
	cvNearParamList.setLength( numCVs );

	hArrBindPreMatrix.jumpToElement( 0 );
	for( int i=0; i< numMatrix; i++ )
	{
		MDataHandle hBindPreMatrix = hArrBindPreMatrix.inputValue();
		MMatrix matrix = hBindPreMatrix.asMatrix().inverse();
		MPoint matrixPoint( matrix(3,0), matrix(3,1), matrix(3,2) );
		matrixPoint *= mtxInputCurve;
		fnCurve.closestPoint( matrixPoint, &matrixNearParamList[i] );
		hArrBindPreMatrix.next();
	}
	for( int i=0; i< numCVs; i++ )
	{
		MPoint cvPoint;
		fnCurve.getCV( i, cvPoint );
		fnCurve.closestPoint( cvPoint, &cvNearParamList[i] );
	}

	MArrayDataBuilder bArrWeightList( aWeightList, numCVs, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	for( int i =0; i< beforeNumCV; i++ )
	{
		delete []setWeights[i];
	}
	delete []setWeights;

	setWeights = new float*[ numCVs ];

	for( int i =0; i< numCVs; i++ )
	{
		setWeights[i] = new float[ numMatrix ];
		for( int j=0; j < numMatrix; j++ )
			setWeights[i][j] = 0.0f;
	}

	for( int i =0; i< numCVs; i++ )
	{
		int smallerIndex = -1;
		int biggerIndex = -1;

		for( int j=0; j<numMatrix; j++ )
		{
			if( cvNearParamList[i] > matrixNearParamList[j] )
			{
				smallerIndex = j;
			}
			else
			{
				biggerIndex = j;
				break;
			}
		}

		if( smallerIndex == -1 )
		{
			hArrBindPreMatrix.jumpToElement( biggerIndex );
			int bindPreBiggerIndex = hArrBindPreMatrix.elementIndex();

			setWeights[i][bindPreBiggerIndex] = 1.0f;
			//printf( "setWeight %2d - %2d %2d : %4.2f, %4.2f\n", i, bindPreBiggerIndex, bindPreBiggerIndex , setWeights[i][bindPreBiggerIndex], setWeights[i][bindPreBiggerIndex] );
		}
		else if( biggerIndex == -1 )
		{
			hArrBindPreMatrix.jumpToElement( smallerIndex );
			int bindPreSmallerIndex = hArrBindPreMatrix.elementIndex();

			setWeights[i][bindPreSmallerIndex] = 1.0f;
			//printf( "setWeight %2d - %2d %2d : %4.2f, %4.2f\n", i, bindPreSmallerIndex, bindPreSmallerIndex , setWeights[i][bindPreSmallerIndex] , setWeights[i][bindPreSmallerIndex]  );
		}
		else
		{
			double smallerParam = matrixNearParamList[ smallerIndex ];
			double currentParam = cvNearParamList[ i ];
			double biggerParam  = matrixNearParamList[ biggerIndex ];

			double leftLength = ( currentParam - smallerParam );
			double rightLength = ( biggerParam - currentParam );
			double allLength = leftLength + rightLength;

			hArrBindPreMatrix.jumpToElement( smallerIndex );
			int bindPreSmallerIndex = hArrBindPreMatrix.elementIndex();

			setWeights[i][bindPreSmallerIndex] = rightLength/allLength;

			hArrBindPreMatrix.jumpToElement( biggerIndex );
			int bindPreBiggerIndex = hArrBindPreMatrix.elementIndex();

			setWeights[i][bindPreBiggerIndex] = leftLength/allLength;

			//printf( "setWeight %2d - %2d %2d : %4.2f, %4.2f\n", i, bindPreSmallerIndex, bindPreBiggerIndex , rightLength/allLength, leftLength/allLength );
		}
	}
	beforeNumCV = numCVs;
	beforeNumMatrix = numMatrix;

	return MS::kSuccess;
}

MStatus  clusterControledCurve::setDependentsDirty( const MPlug &plug, MPlugArray& plugArray )
{
	if ( plug.partialName() == "bindPreMatrix" )
	{
	   	requireUpdate = true;
    }
	else if ( plug.partialName() == "dumyMatrix" )
	{
	   	requireUpdate = true;
    }
	return MS::kSuccess;
}