#include "sgWobbleCurve.h"

#define  HALF_PI  1.57079632679


MStatus sgWobbleCurve::clearCurveDirty( MDataBlock& data )
{
	MStatus status;

	MFnNurbsCurve fnCurve = data.inputValue( aInputCurve ).asNurbsCurve();
	int numCVs = fnCurve.numCVs();
	int degrees = fnCurve.degree();

	if( numCVs != m_numCVs || degrees != m_degrees )
	{
		MPointArray pointCVs;
		MDoubleArray knots;
		fnCurve.getCVs( m_pointsInputCurve );
		fnCurve.getKnots( knots );

		MFnNurbsCurveData curveData;
		m_outputCurve = curveData.create();
		fnCurve.create( m_pointsInputCurve, knots, degrees, fnCurve.form(), false, false, m_outputCurve, &status );

		m_numCVs = numCVs;
		m_degrees = degrees;
	}
	else
	{
		fnCurve.getCVs( m_pointsInputCurve );
	}
	if( data.inputValue( aApplyCurveLength ).asBool() )
	{
		m_curveLength = fnCurve.length();
	}
	else
		m_curveLength = 1.0;

	return MS::kSuccess;
}



MStatus sgWobbleCurve::clearCurveMatrix( MDataBlock& data )
{
	MStatus status;
	MDataHandle hAimMatrix = data.inputValue( aAimMatrix );
	m_mtxCurve = hAimMatrix.asMatrix();
	return MS::kSuccess;
}



MStatus sgWobbleCurve::clearAimMatrix( MDataBlock& data )
{
	MStatus status;
	MDataHandle hAimMatrix = data.inputValue( aAimMatrix );
	m_mtxAim = hAimMatrix.asMatrix();
	m_mtxLocalAim = m_mtxAim * m_mtxCurve.inverse();
	m_mtxLocalAim( 3,0 ) = 0.0;
	m_mtxLocalAim( 3,1 ) = 0.0;
	m_mtxLocalAim( 3,2 ) = 0.0;
	return MS::kSuccess;
}


MStatus sgWobbleCurve::clearEndRate( MDataBlock& data )
{
	MStatus status;
	MDataHandle hEndRate = data.inputValue( aPinEndRate );
	m_endRate = hEndRate.asFloat();
	return MS::kSuccess;
}


MStatus sgWobbleCurve::clearAimIndex( MDataBlock& data )
{
	MStatus status;
	MDataHandle hIndexAxis = data.inputValue( aAimIndex );
	m_indexAxis = hIndexAxis.asUChar();
	return MS::kSuccess;
}


MStatus sgWobbleCurve::clearWaves( MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrWaves = data.inputArrayValue( aWaves );
	MArrayDataHandle hArrWaveOptions = data.inputArrayValue( aWaveOptions );
	MTime time = data.inputValue( aTime ).asTime();

	MRampAttribute rAttr( thisMObject(), aFallOff );

	int lengthWaves = hArrWaves.elementCount();
	int lengthOptions = hArrWaveOptions.elementCount();

	int length;
	if( lengthWaves > lengthOptions )
		length = lengthOptions;
	else
		length = lengthWaves;

	int pointLength = m_pointsInputCurve.length();
	m_dArrRate1.setLength( pointLength );
	m_dArrRate2.setLength( pointLength );
	for( int i=0; i< pointLength; i++ )
	{
		m_dArrRate1[i] = 0.0;
		m_dArrRate2[i] = 0.0;
	}
	if( pointLength-1 <= 0 ) return MS::kFailure;

	float rampValue;
	for( int i=0; i< length; i++, hArrWaves.next(), hArrWaveOptions.next() )
	{
		MDataHandle hWave = hArrWaves.inputValue();
		MDataHandle hWaveOptions = hArrWaveOptions.inputValue();

		double rate1 = hWave.child( aRate1 ).asDouble();
		double rate2 = hWave.child( aRate2 ).asDouble();
		double offset = hWaveOptions.child( aOffset ).asDouble();
		double waveLength = hWaveOptions.child( aWaveLength ).asDouble();
		double timeMult   = hWaveOptions.child( aTimeMult ).asDouble();

		for( int j=0; j<pointLength; j++ )
		{
			double eachOffset = j/( pointLength-1.0 );
			rAttr.getValueAtPosition( eachOffset, rampValue );
			m_dArrRate1[j] += (sin( ( offset + eachOffset + time.value()*timeMult/m_curveLength ) / waveLength *m_curveLength )*rate1*rampValue) *m_envelope;
			m_dArrRate2[j] += (sin( ( offset + eachOffset + time.value()*timeMult/m_curveLength ) / waveLength *m_curveLength )*rate2*rampValue) *m_envelope;
		}
	}

	return MS::kSuccess;
}


MStatus sgWobbleCurve::setResult( MDataBlock& data )
{
	MStatus status;

	MFnNurbsCurve fnCurve( m_outputCurve );
	fnCurve.setCVs( m_pointsResult );
	data.outputValue( aOutputCurve ).set( m_outputCurve );

	return MS::kSuccess;
}


MStatus sgWobbleCurve::getEachPointMatrix()
{
	MStatus status;

	int lengthPoint = m_pointsInputCurve.length();

	MMatrix mtxBase = m_mtxAim;
	
	m_mtxArrEachPoint.setLength( lengthPoint );
	for( int i=0; i< lengthPoint-1; i++ )
	{
		MPoint& pointPiv = m_pointsInputCurve[i];
		MPoint& pointAim = m_pointsInputCurve[i+1];

		MVector vAim = pointAim - pointPiv;

		m_mtxArrEachPoint[i] = getAimVectorMatrix( mtxBase, vAim, pointPiv, m_indexAxis );
		mtxBase = m_mtxArrEachPoint[i];
	}
	int lastIndex = lengthPoint-1;
	m_mtxArrEachPoint[ lastIndex ] = m_mtxArrEachPoint[ lengthPoint -2 ];
	m_mtxArrEachPoint[ lastIndex ](3,0) = m_pointsInputCurve[ lastIndex ].x;
	m_mtxArrEachPoint[ lastIndex ](3,1) = m_pointsInputCurve[ lastIndex ].y;
	m_mtxArrEachPoint[ lastIndex ](3,2) = m_pointsInputCurve[ lastIndex ].z;

	return MS::kSuccess;
}



MStatus sgWobbleCurve::getEachAngleMatrix()
{
	MStatus status;

	int lengthPoint = m_pointsInputCurve.length();
	m_mtxArrEachAngle.setLength( lengthPoint );

	for( int i=0; i< lengthPoint; i++ )
	{
		m_mtxArrEachAngle[i] = getAngledMatrix( m_dArrRate1[i], m_dArrRate2[i], m_indexAxis );
	}

	return MS::kSuccess;
}


MStatus sgWobbleCurve::editPointsByMatrixMult()
{
	MStatus status;

	int lengthPoint = m_pointsInputCurve.length();
	m_pointsResult = m_pointsInputCurve;
	
	MMatrixArray mtxMultedEachPoints;
	mtxMultedEachPoints = m_mtxArrEachPoint;

	for( int i=0; i< lengthPoint-1; i++ )
	{
		MMatrix mtxMult = mtxMultedEachPoints[i].inverse() * m_mtxArrEachAngle[i] * mtxMultedEachPoints[i];
		
		for( int j=i+1; j< lengthPoint; j++ )
			m_pointsResult[j] *= mtxMult;
		for( int j=i+1; j< lengthPoint-1; j++ )
			mtxMultedEachPoints[j] *= mtxMult;
	}

	return MS::kSuccess;
}


MStatus sgWobbleCurve::editPoints()
{
	MStatus status;

	int lengthPoint = m_pointsInputCurve.length();
	m_pointsResult = m_pointsInputCurve;
	
	MMatrixArray mtxMultedEachPoints;
	mtxMultedEachPoints = m_mtxArrEachPoint;

	for( int i=0; i< lengthPoint-1; i++ )
	{
		MVector vPoint = m_pointsResult[i+1]-m_pointsResult[i];
		MPoint addPoint = vPoint * m_mtxAim.inverse() * m_mtxArrEachAngle[i] * m_mtxAim - vPoint;
		
		float endRate = m_endRate/(lengthPoint-i);
		for( int j=i+1; j< lengthPoint; j++ )
			m_pointsResult[j] += addPoint*( 1.0f-endRate*(j-i) );
	}

	return MS::kSuccess;
}


MMatrix sgWobbleCurve::getAimVectorMatrix( MMatrix mtxBase, MVector vInputAim, MPoint pointStart, unsigned int indexAxis )
{
	vInputAim.normalize();

	bool axisIsInverse = false;
	if( indexAxis >= 3 )
	{
		axisIsInverse = true;
	}
	int indexPositiveAxis = ( indexAxis + 3 ) % 3;
	int indexUpAxis1      = ( indexPositiveAxis +1 ) % 3;
	int indexUpAxis2      = ( indexPositiveAxis +2 ) % 3;

	MVector vUp1 = mtxBase[ indexUpAxis1 ];
	MVector vUp2 = mtxBase[ indexUpAxis2 ];
	vUp2.normalize();
	MVector vAim = mtxBase[ indexPositiveAxis ];

	if( axisIsInverse )
	{
		vAim *= -1;
		vUp1 *= -1;
	}

	double dotUp1 = vInputAim * vUp1;
	double dotUp2 = vInputAim * vUp2;
	double dotAim = vInputAim * vAim;

	double allDot = fabs( dotUp1 ) + fabs( dotUp2 );
	if( allDot == 0.0001 ) 
	{
		dotUp1 = 1.0;
		dotUp2 = 0.0;
		allDot = 1.0;
	}
	double dotUpRate1 = fabs( dotUp1 )/allDot;
	double dotUpRate2 = fabs( dotUp2 )/allDot;

	vUp1 = dotAim*vUp1 - dotUp1*vAim;
	vUp2 = dotAim*vUp2 - dotUp2*vAim;
	MVector vCross2 =  vUp2 ^ vInputAim;
	vUp1.normalize();
	vCross2.normalize();

	MVector vUp = vUp1 * dotUpRate1 + vCross2 * dotUpRate2;
	MVector vCross = vInputAim ^ vUp;
	vUp = vCross ^ vInputAim;

	MMatrix mtxResult;
	mtxResult(indexPositiveAxis,0) = vInputAim.x;
	mtxResult(indexPositiveAxis,1) = vInputAim.y;
	mtxResult(indexPositiveAxis,2) = vInputAim.z;
	mtxResult(indexUpAxis1,0) = vUp.x;
	mtxResult(indexUpAxis1,1) = vUp.y;
	mtxResult(indexUpAxis1,2) = vUp.z;
	mtxResult(indexUpAxis2,0) = vCross.x;
	mtxResult(indexUpAxis2,1) = vCross.y;
	mtxResult(indexUpAxis2,2) = vCross.z;
	mtxResult( 3, 0 ) = pointStart.x;
	mtxResult( 3, 1 ) = pointStart.y;
	mtxResult( 3, 2 ) = pointStart.z;

	return mtxResult;
}


MMatrix sgWobbleCurve::getAngledMatrix( double angle1, double angle2, unsigned int indexAxis )
{
	double angleRate1 = angle1 / 90;
	double angleRate2 = angle2 / 90;
	double allRate = fabs( angleRate1 ) + fabs( angleRate2 );
	double invRate = 1.0 - allRate;

	bool axisIsInverse = false;
	if( indexAxis >= 3 )
	{
		axisIsInverse = true;
	}
	int indexPositiveAxis = ( indexAxis + 3 ) % 3;
	int indexUpAxis1      = ( indexPositiveAxis +1 ) % 3;
	int indexUpAxis2      = ( indexPositiveAxis +2 ) % 3;

	MMatrix mtxDefault;
	MVector vAim = MVector( mtxDefault[ indexPositiveAxis ] )*invRate;
	MVector vUp1 = MVector( mtxDefault[ indexUpAxis1 ] )*angleRate1;
	MVector vUp2 = MVector( mtxDefault[ indexUpAxis2 ] )*angleRate2;

	MVector vMainAim = vAim + vUp1 + vUp2;

	MVector vMainUp1;
	vMainUp1[ indexPositiveAxis ] = -vMainAim[ indexUpAxis1 ];
	vMainUp1[ indexUpAxis1 ] = vMainAim[ indexPositiveAxis ];
	vMainUp1[ indexUpAxis2 ] = 0.0;

	MVector vMainUp2;
	vMainUp2[ indexPositiveAxis ] = -vMainAim[ indexUpAxis2 ];
	vMainUp2[ indexUpAxis1 ] = 0.0;
	vMainUp2[ indexUpAxis2 ] = vMainAim[ indexPositiveAxis ];

	MVector vMainCross1 = vMainUp2 ^ vMainAim;

	vMainUp1.normalize();
	vMainCross1.normalize();

	double dotUp1 = vMainAim * MVector( mtxDefault[ indexUpAxis1 ] );
	double dotUp2 = vMainAim * MVector( mtxDefault[ indexUpAxis2 ] );
	double dotAim = vMainAim * MVector( mtxDefault[ indexPositiveAxis ] );

	double allDot = fabs( dotUp1 ) + fabs( dotUp2 );
	if( allDot < 0.0001 ) 
	{
		dotUp1 = 1.0;
		dotUp2 = 0.0;
		allDot = 1.0;
	}
	double dotUpRate1 = fabs( dotUp1 )/allDot;
	double dotUpRate2 = fabs( dotUp2 )/allDot;

	vMainAim.normalize();
	MVector vMainUp = vMainUp1 * dotUpRate1 + vMainCross1 * dotUpRate2;
	MVector vMainCross = vMainAim ^ vMainUp;
	vMainCross.normalize();
	vMainUp = vMainCross ^ vMainAim;

	if( axisIsInverse )
	{
		vMainAim   *= -1;
		vMainUp    *= -1;
		vMainCross *= -1;
	}

	MMatrix mtxReturn;

	mtxReturn(indexPositiveAxis,0) = vMainAim.x;
	mtxReturn(indexPositiveAxis,1) = vMainAim.y;
	mtxReturn(indexPositiveAxis,2) = vMainAim.z;

	mtxReturn(indexUpAxis1,0) = vMainUp.x;
	mtxReturn(indexUpAxis1,1) = vMainUp.y;
	mtxReturn(indexUpAxis1,2) = vMainUp.z;

	mtxReturn(indexUpAxis2,0) = vMainCross.x;
	mtxReturn(indexUpAxis2,1) = vMainCross.y;
	mtxReturn(indexUpAxis2,2) = vMainCross.z;

	return mtxReturn;
}