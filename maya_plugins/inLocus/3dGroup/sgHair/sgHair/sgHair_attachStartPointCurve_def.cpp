#include  "sgHair_attachStartPointCurve.h"

MStatus sgHair_attachStartPointCurve::checkAndCreateCurveAndGetPosition()
{
	MStatus status;

	MFnNurbsCurve fnCurve( m_oInputCurve );

	if( m_numCVs != fnCurve.numCVs() )
	{
		MFnNurbsCurveData curveData;
		m_oOutCurve = curveData.create();
		
		MPointArray pArr;
		MDoubleArray dArr;
		dArr.setLength( fnCurve.numCVs() );

		fnCurve.getCVs( pArr );

		for( int i=0; i < fnCurve.numCVs(); i++ )
		{
			dArr[i] = ( double )i;
		}

		fnCurve.create( pArr, dArr, 1, MFnNurbsCurve::kOpen, false, false, m_oOutCurve, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		m_fnCurve.setObject( m_oOutCurve );
		m_numCVs = fnCurve.numCVs();
	}

	fnCurve.getCVs( m_outputPoints );

	if( m_mtxInputCurve != MMatrix() )
	{
		for( int i=0; i< m_outputPoints.length(); i++ )
			m_outputPoints[i] *= m_mtxInputCurve;
	}

	return MS::kSuccess;
}



MStatus sgHair_attachStartPointCurve::editPositionByMatrix()
{
	MStatus status;

	MPoint pointInput( m_mtxInput( 3, 0 ), m_mtxInput( 3, 1 ), m_mtxInput( 3, 2 ) );
	
	MVector vOffset = pointInput - m_outputPoints[0];
	double eachOffsetValue = 1.0 / (m_outputPoints.length()-1);

	double offsetValue;
	for( int i=0; i< m_outputPoints.length(); i++ )
	{
		offsetValue = eachOffsetValue * ( m_outputPoints.length()-1 -i );
		m_outputPoints[i] += offsetValue * vOffset;
	}

	m_fnCurve.setCVs( m_outputPoints );

	return MS::kSuccess;
}