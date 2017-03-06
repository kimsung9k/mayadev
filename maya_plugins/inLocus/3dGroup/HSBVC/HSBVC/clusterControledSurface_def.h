#ifndef _clusterControledSurface_def_h
#define _clusterControledSurface_def_h

#include "clusterControledSurface.h"

MStatus clusterControledSurface::updateBaseUpMatrix(MObject     oInputOrigCurve,
	                                                MMatrix&     mtxInputOrigCurve,
	                                                MArrayDataHandle& hArrUpMatrix, 
													MArrayDataHandle& hArrBaseUpMatrix,
													bool checkPoint )
{
	MStatus status;

	int numUpMatrix = hArrUpMatrix.elementCount();
	int numBaseUpMatrix = hArrBaseUpMatrix.elementCount();

	if( oInputOrigCurve.isNull() )
		return MS::kFailure;

	MFnNurbsCurve fnInputOrigCurve = oInputOrigCurve;

	double minParam = fnInputOrigCurve.findParamFromLength( 0.0 );
	double maxParam = fnInputOrigCurve.findParamFromLength( fnInputOrigCurve.length() );

	if( numUpMatrix > numBaseUpMatrix )
	{
		MArrayDataBuilder bArrBaseUpMatrix( aBaseUpMatrix, numUpMatrix );
		
		hArrUpMatrix.jumpToElement( 0 );
		for( int i=0; i<numUpMatrix; i++ )
		{
			MDataHandle hUpMatrix = hArrUpMatrix.inputValue();
			MDataHandle hBaseUpMatrix = bArrBaseUpMatrix.addElement( hArrUpMatrix.elementIndex() );
			hBaseUpMatrix.set( hUpMatrix.asMatrix() );
			hArrUpMatrix.next();
		}
		hArrBaseUpMatrix.set( bArrBaseUpMatrix );
		hArrBaseUpMatrix.setAllClean();
	}

	inBaseUpMatrix.setLength( numUpMatrix );
	inParamPerMatrix.setLength( numUpMatrix );

	hArrBaseUpMatrix.jumpToElement( 0 );
	
	MMatrix baseUpMatrix;
	MPoint baseUpPoint;
	MPoint closePoint;
	double paramPerMatrix;

	for( int i=0; i<numUpMatrix; i++ )
	{
		MDataHandle hBaseUpMatrix = hArrBaseUpMatrix.inputValue();

		baseUpMatrix = hBaseUpMatrix.asMatrix();

		if( baseUpMatrix != inBaseUpMatrix[i] )
		{
			MPoint baseUpPoint( baseUpMatrix( 3,0 ), baseUpMatrix( 3,1 ), baseUpMatrix( 3,2 ) );
			closePoint = fnInputOrigCurve.closestPoint( baseUpPoint );
			fnInputOrigCurve.getParamAtPoint( closePoint, paramPerMatrix );
			inBaseUpMatrix.set( baseUpMatrix, i );
			inParamPerMatrix.set( paramPerMatrix, i );

			baseUpMatrixChanged = true;
		}
		hArrBaseUpMatrix.next();
	}


	return MS::kSuccess; 
};


bool   checkTwoSurfaceIsSameLevel( MObject *first, MObject *second )
{
	MFnNurbsSurface fnFirst( *first );
	MFnNurbsSurface fnSecond( *second );

	if( fnFirst.numCVsInU() != fnSecond.numCVsInU() )
		return false;
	if( fnFirst.numCVsInV() != fnSecond.numCVsInV() )
		return false;
	if( fnFirst.degreeU() != fnSecond.degreeU() )
		return false;
	if( fnFirst.degreeV() != fnSecond.degreeV() )
		return false;

	return true;
}

bool   checkTwoCurveIsSameLevel( MObject *first, MObject *second )
{
	MFnNurbsCurve fnFirst( *first );
	MFnNurbsCurve fnSecond( *second );

	if( fnFirst.numCVs() != fnSecond.numCVs() )
		return false;
	if( fnFirst.degree() != fnSecond.degree() )
		return false;

	return true;
}

bool   checkTwoSurfaceIsSamePoints( MObject *first, MObject *second )
{
	MItSurfaceCV itFirst( *first, false );
	MItSurfaceCV itSecond( *second, false );

	int iterIndex;
	MPoint firstPoint;
	MPoint secondPoint;

	while( !itFirst.isDone() )
	{
		while( !itFirst.isRowDone() )
		{
			iterIndex = itFirst.index();

			firstPoint = itFirst.position();
			secondPoint = itSecond.position();

			if( firstPoint != secondPoint )
			{
				return false;
			}

			itFirst.next();
			itSecond.next();
		}
		itFirst.nextRow();
		itSecond.nextRow();
	}

	return true;
}

bool   checkTwoCurveIsSamePoints( MObject *first, MObject *second )
{
	MItCurveCV itFirst( *first, false );
	MItCurveCV itSecond( *second, false );

	while( !itFirst.isDone() )
	{
		if( itFirst.position() != itSecond.position() )
			return false;
		itFirst.next();
		itSecond.next();
	}
	return true;
}


MMatrix getMatrixFromParamAndUpMatrix( MVector aimVector, MPoint pivPoint, MMatrixArray& upMatrix, MDoubleArray& inParamPerMatrix, double parameter )
{
	int paramPerMatrixLength = inParamPerMatrix.length();

	if( !paramPerMatrixLength || upMatrix.length() < paramPerMatrixLength )
		return MMatrix();

	int minIndex = -1;
	int maxIndex = -1;
	double currentParam;

	for( int i=0; i<paramPerMatrixLength; i++ )
	{
		currentParam = inParamPerMatrix[i];
		if( parameter > currentParam )
		{
			minIndex = i;
		}
		else
		{
			maxIndex = i;
			break;
		}
	}
	double leftWeight;
	double rightWeight;

	MMatrix minMatrix;
	MMatrix maxMatrix;

	MVector weightedUpVector;

	if( minIndex == -1 )
	{
		minMatrix = upMatrix[maxIndex];
		weightedUpVector = MVector( minMatrix(1,0), minMatrix(1,1), minMatrix(1,2) );
	}
	else if( maxIndex == -1 )
	{
		maxMatrix = upMatrix[minIndex];
		weightedUpVector = MVector( maxMatrix(1,0), maxMatrix(1,1), maxMatrix(1,2) );
	}
	else
	{
		MMatrix minMatrix = upMatrix[minIndex];
		MMatrix maxMatrix = upMatrix[maxIndex];

		double leftLength = parameter - inParamPerMatrix[ minIndex ];
		double rightLength = inParamPerMatrix[ maxIndex ] - parameter;
		double allLength = leftLength + rightLength;

		leftWeight = rightLength/allLength;
		rightWeight = leftLength/allLength;

		MVector leftUpVector( minMatrix(1,0), minMatrix(1,1), minMatrix(1,2) );
		MVector rightUpVector( maxMatrix(1,0), maxMatrix(1,1), maxMatrix(1,2) );

		weightedUpVector = leftUpVector*leftWeight + rightUpVector*rightWeight;
	}

	MVector byNormal = aimVector^weightedUpVector;
	MVector upVector = byNormal^aimVector;

	aimVector.normalize();
	upVector.normalize();
	byNormal.normalize();

	double buildMatrix[4][4] = { aimVector.x, aimVector.y, aimVector.z, 0,
		                         upVector.x,  upVector.y,  upVector.z,  0,
								 byNormal.x,  byNormal.y,  byNormal.z,  0,
								 pivPoint.x,  pivPoint.y,  pivPoint.z,  1 };

	return MMatrix( buildMatrix );
}


MStatus clusterControledSurface::updateInputSurfaceInfo( MObject oInputOrigCurve, MObject oInputSurface, 
														 MMatrix mtxOrigCurve, MMatrix mtxSurface, 
														 bool checkPoint )
{
	if( oInputOrigCurve.isNull() || oInputSurface.isNull() )
	{
		return MS::kFailure;
	}
	if( inOrigCurve.isNull() || inSurface.isNull() )
	{
		inOrigCurve = oInputOrigCurve;
		inSurface   = oInputSurface;
	}
	MFnNurbsSurface fnInputSurface( oInputSurface );
	int numCVsInU = fnInputSurface.numCVsInU();
	int numCVsInV = fnInputSurface.numCVsInV();

	bool surfaceIsSameLevel = checkTwoSurfaceIsSameLevel( &oInputSurface, &inSurface );
	bool curveIsSameLevel   = checkTwoCurveIsSameLevel( &oInputOrigCurve, &inOrigCurve );

	if( surfaceIsSameLevel && curveIsSameLevel )
	{
		if( inParamPerPoints.length() >= numCVsInU*numCVsInV && !( baseUpMatrixChanged && checkPoint && upMatrixChangeAble ) )
		{
			return MS::kSuccess;
		}

		bool surfaceIsSamePoints = checkTwoSurfaceIsSamePoints( &oInputSurface, &inSurface );
		bool curveIsSamePoints   = checkTwoCurveIsSamePoints( &oInputOrigCurve, &inOrigCurve );
	}

	MFnNurbsCurve fnOrigCurve = oInputOrigCurve;
	double minParam = fnOrigCurve.findParamFromLength( 0 );
	double maxParam = fnOrigCurve.findParamFromLength( fnOrigCurve.length() );
	double paramLength = maxParam - minParam;

	MItSurfaceCV itSurface( oInputSurface, false );
	MFnNurbsSurface fnSurface( oInputSurface );

	int cvLength = fnSurface.numCVsInU()*fnSurface.numCVsInV();

	inPoints.setLength( cvLength );
	inParamPerPoints.setLength( cvLength );

	MPoint iterPoint;
	MPoint  localIterPoint;
	MPoint closePoint;
	int iterIndex;
	double closeParam;

	MMatrix mtxInPoint;
	MVector aimVector;
	MPoint  pivPoint;

	for( ;!itSurface.isDone();itSurface.nextRow() )
	{
		for( ;!itSurface.isRowDone(); itSurface.next() )
		{
			iterIndex = itSurface.index();
			iterPoint = itSurface.position()*mtxSurface;
			localIterPoint = iterPoint*mtxOrigCurve.inverse();
			closePoint = fnOrigCurve.closestPoint( localIterPoint );
			fnOrigCurve.getParamAtPoint( closePoint, closeParam );
			inParamPerPoints[ iterIndex ] = ( closeParam - minParam )/paramLength;
			aimVector = fnOrigCurve.tangent( closeParam )*mtxOrigCurve;
			fnOrigCurve.getPointAtParam( closeParam, pivPoint )*mtxOrigCurve;
			mtxInPoint = getMatrixFromParamAndUpMatrix( aimVector, pivPoint, inBaseUpMatrix, inParamPerMatrix, closeParam );
			inPoints[ iterIndex ] = iterPoint*mtxInPoint.inverse();
		}
	}
	numCVs = iterIndex;

	inOrigCurve = oInputOrigCurve;
	inSurface   = oInputSurface;

	baseUpMatrixChanged = false;

	return MS::kSuccess;
}


MStatus  clusterControledSurface::moveSurfacePoints( MObject oInputCurve,
	                                                 MObject oOutputSurface, 
	                                                 MMatrix mtxCurve,
	                                                 MMatrix mtxSurface, 
													 MArrayDataHandle& hArrUpMatrix )
{
	if( oOutputSurface.isNull() || oInputCurve.isNull()  )
	{
		return MS::kFailure;
	}

	int upMatrixCount = hArrUpMatrix.elementCount();
	MMatrixArray arrUpMatrix;
	arrUpMatrix.setLength( upMatrixCount );

	hArrUpMatrix.jumpToElement( 0 );
	for( int i=0; i<upMatrixCount; i++ )
	{
		arrUpMatrix[i] = hArrUpMatrix.inputValue().asMatrix();
		hArrUpMatrix.next();
	}

	MItSurfaceCV itSurface( oOutputSurface, false );
	MFnNurbsSurface fnSurface( oOutputSurface );
	int cvLength = fnSurface.numCVsInU()*fnSurface.numCVsInV();

	MFnNurbsCurve  fnCurve( oInputCurve );

	double minParam = fnCurve.findParamFromLength( 0 );
	double maxParam = fnCurve.findParamFromLength( fnCurve.length() );
	double paramLength = maxParam - minParam;

	int iterIndex;
	MPoint iterPoint;
	MPoint localIterPoint;
	MPoint closePoint;

	MVector aimVector;
	MPoint pivPoint;

	double closeParam;

	MMatrix mtxInPoint;

	int paramPerPointLength = inParamPerPoints.length();

	MMatrix mtxSurfaceInverse = mtxSurface.inverse();

	for( ;!itSurface.isDone();itSurface.nextRow() )
	{
		for( ;!itSurface.isRowDone(); itSurface.next() )
		{
			iterIndex = itSurface.index();

			closeParam = inParamPerPoints[ iterIndex ]*paramLength + minParam;

			aimVector = fnCurve.tangent( closeParam )*mtxCurve;
			fnCurve.getPointAtParam( closeParam, pivPoint )*mtxCurve;
			mtxInPoint = getMatrixFromParamAndUpMatrix( aimVector, pivPoint, arrUpMatrix, inParamPerMatrix, closeParam );
			itSurface.setPosition( inPoints[ iterIndex ]* mtxInPoint * mtxSurfaceInverse );
		}
	}
	return MS::kSuccess;
}


#endif