#include "sgHair_controledCurveB.h"


MTypeId sgHair_controledCurveB::id( 0x20150303 );

MObject sgHair_controledCurveB::aInputMatrix;
MObject sgHair_controledCurveB::aParentInverseMatrix;
MObject sgHair_controledCurveB::aOutputCurve;


void* sgHair_controledCurveB::creator()
{
	return new sgHair_controledCurveB();
}


sgHair_controledCurveB::sgHair_controledCurveB()
{
	m_numInputMatrix = 0;
}


sgHair_controledCurveB::~sgHair_controledCurveB()
{

}


MStatus sgHair_controledCurveB::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrInputMatrix = data.inputValue( aInputMatrix );
	int numInputMatrix = hArrInputMatrix.elementCount();

	m_pArrPosition.setLength( numInputMatrix );
	m_dArrKnots.setLength( numInputMatrix );
	MMatrix mtxInputMatrix;
	for( int i=0; i< numInputMatrix; i++, hArrInputMatrix.next() )
	{
		mtxInputMatrix = hArrInputMatrix.inputValue().asMatrix();
		m_pArrPosition[i].x = mtxInputMatrix( 3,0 );
		m_pArrPosition[i].y = mtxInputMatrix( 3,1 );
		m_pArrPosition[i].z = mtxInputMatrix( 3,2 );
		m_dArrKnots[i] = double( i );
	}

	if( numInputMatrix != m_numInputMatrix )
	{
		MFnNurbsCurveData dataCurve;
		m_oDataCurve = dataCurve.create();
		m_fnCurve.create( m_pArrPosition, m_dArrKnots, 1, MFnNurbsCurve::kOpen , false, false, m_oDataCurve, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_fnCurve.setObject( m_oDataCurve );
		m_numInputMatrix = numInputMatrix;
	}

	MDataHandle hParentInverseMatrix = data.inputValue( aParentInverseMatrix );
	MMatrix mtxParentInverse = hParentInverseMatrix.asMatrix();

	if( mtxParentInverse != MMatrix() )
	{
		m_pArrPositionLocal.setLength( m_pArrPosition.length() );
		for( int i=0; i< m_pArrPosition.length(); i++ )
			m_pArrPositionLocal[i] = m_pArrPosition[i] * mtxParentInverse;
	}
	else
	{
		m_pArrPositionLocal = m_pArrPosition;
	}

	m_fnCurve.setCVs( m_pArrPosition );

	MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
	hOutputCurve.setMObject( m_oDataCurve );

	data.setClean( plug );

	return MS::kSuccess;
}


MStatus sgHair_controledCurveB::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	return MS::kSuccess;
}


MStatus sgHair_controledCurveB::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnMessageAttribute msgAttr;
	MFnNumericAttribute nAttr;


	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	mAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMatrix ) );

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aParentInverseMatrix ) );

	aOutputCurve = tAttr.create( "outputCurve", "outCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutputCurve ) );

	return MS::kSuccess;
}