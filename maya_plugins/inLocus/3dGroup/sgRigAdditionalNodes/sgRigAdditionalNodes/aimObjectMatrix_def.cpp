#include "aimObjectMatrix.h"

#define HALFPI 1.57079632679


MStatus aimObjectMatrix::getMatrixByCurve()
{
	if( !m_fnCurve.numCVs() )
		return MS::kFailure;
	MPoint mtxPos = m_mtxBase[3];
	mtxPos *= m_mtxCurve.inverse();

	double param;
	MPoint closePoint = m_fnCurve.closestPoint( mtxPos, false, &param );

	MVector tangent = m_fnCurve.tangent( param );
	tangent.normalize();

	if( m_aimIndex > 2 )
	{
		tangent *= -1;
	}

	MPoint mtxPoint = closePoint + tangent;

	mtxPoint *= m_mtxCurve;
	closePoint *= m_mtxCurve;

	m_mtxTarget( 3, 0 ) = mtxPoint.x;
	m_mtxTarget( 3, 1 ) = mtxPoint.y;
	m_mtxTarget( 3, 2 ) = mtxPoint.z;
	m_mtxBase( 3, 0 ) = closePoint.x;
	m_mtxBase( 3, 1 ) = closePoint.y;
	m_mtxBase( 3, 2 ) = closePoint.z;
}


MStatus aimObjectMatrix::caculate()
{
	MStatus status;

	MPoint point = m_mtxTarget[3];
	MVector vPoint;
	vPoint = point*m_mtxBase.inverse();
	vPoint.normalize();

	if( m_inverseAim )
	{
		vPoint *= -1;
	}

	double aimBase[3] = {0,0,0};
	double upBase[3]  = {0,0,0};

	int aimIndex = m_aimIndex%3;
	int upIndex  = m_upIndex%3;
	int crossIndex = 3 - aimIndex - upIndex;

	aimBase[ aimIndex ] = 1;
	upBase[ upIndex ] = 1;

	MVector vAimBase( aimBase );
	MVector vUpBase( upBase );
	MVector vCrossBase = vAimBase ^ vUpBase;

	MVector vUp1( 0,0,0 );
	vUp1[ aimIndex ] = -vPoint[ upIndex ];
	vUp1[ upIndex ] = vPoint[ aimIndex ];
	MVector vCross2( 0,0,0 );
	vCross2[ aimIndex ] = -vPoint[ crossIndex ];
	vCross2[ crossIndex ] = vPoint[ aimIndex ];

	MVector vUp2 = vCross2 ^ vPoint;
	MVector vCross1 = vPoint ^ vUp1;

	double upRate = fabs( vPoint[ upIndex ] );
	double crossRate = fabs( vPoint[ crossIndex ] );

	double divRate = upRate + crossRate;
	
	double firstWeight, secondWeight;
	if( divRate < 0.0001 )
	{
		firstWeight = 1.0;
		secondWeight = 0.0;
	}
	else
	{
		firstWeight = upRate / divRate;
		secondWeight = crossRate / divRate;
	}

	MVector vUp    = vUp1 * firstWeight + vUp2 * secondWeight;

	MVector vCross = vPoint ^ vUp;

	double mtxBuild[4][4];
	mtxBuild[ aimIndex ][0] = vPoint.x;
	mtxBuild[ aimIndex ][1] = vPoint.y;
	mtxBuild[ aimIndex ][2] = vPoint.z;
	mtxBuild[ aimIndex ][3] = 0.0;

	mtxBuild[ upIndex  ][0] = vUp.x;
	mtxBuild[ upIndex  ][1] = vUp.y;
	mtxBuild[ upIndex  ][2] = vUp.z;
	mtxBuild[ upIndex  ][3] = 0.0;

	mtxBuild[ crossIndex ][0] = vCross.x;
	mtxBuild[ crossIndex ][1] = vCross.y;
	mtxBuild[ crossIndex ][2] = vCross.z;
	mtxBuild[ crossIndex ][3] = 0.0;

	mtxBuild[ 3 ][ 0 ] = 0.0;
	mtxBuild[ 3 ][ 1 ] = 0.0;
	mtxBuild[ 3 ][ 2 ] = 0.0;
	mtxBuild[ 3 ][ 3 ] = 1.0;

	m_mtxOutput = MMatrix( mtxBuild );

	return MS::kSuccess;
}