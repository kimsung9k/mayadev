#include "sgHair_controledCurve.h"


MTypeId sgHair_controledCurve::id( 0x20150225 );

MObject sgHair_controledCurve::aTopJoint;
MObject sgHair_controledCurve::aEndJointMatrix;
MObject sgHair_controledCurve::aUpdateJoint;
MObject sgHair_controledCurve::aParentInverseMatrix;
MObject sgHair_controledCurve::aOutputCurve;


void* sgHair_controledCurve::creator()
{
	return new sgHair_controledCurve();
}


sgHair_controledCurve::sgHair_controledCurve()
{
	m_isDirtyJointMatrix = true;
	m_isDirtyUpdate = true;
}


sgHair_controledCurve::~sgHair_controledCurve()
{

}


MStatus sgHair_controledCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	if( m_isDirtyUpdate )
	{
		MDataHandle hTopJoint = data.inputValue( aTopJoint );
		MDataHandle hUpdateJoint = data.inputValue( aUpdateJoint );
		status = updateObjectArray();
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MFnDependencyNode fnNode( thisMObject() );
		MPlug plugUpdateJoint = fnNode.findPlug( aUpdateJoint );
		if( plugUpdateJoint.asBool() ) plugUpdateJoint.setBool( false );

		status = updateJointPosition();
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MFnNurbsCurveData dataCurve;
		m_oDataCurve = dataCurve.create();
		m_fnCurve.create( m_pArrPosition, m_dArrKnots, 1, MFnNurbsCurve::kOpen , false, false, m_oDataCurve, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_fnCurve.setObject( m_oDataCurve );
	}

	if( m_isDirtyJointMatrix || m_isDirtyUpdate )
	{
		MDataHandle hEndJointMatrix = data.inputValue( aEndJointMatrix );
		status = updateJointPosition();
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	MDataHandle hParentInverseMatrix = data.inputValue( aParentInverseMatrix );
	MMatrix mtxParentInverse = hParentInverseMatrix.asMatrix();
	/*
	m_pArrPositionLocal.setLength( m_pArrPosition.length() );
	for( int i=0; i< m_pArrPosition.length(); i++ )
		m_pArrPositionLocal[i] = m_pArrPosition[i] * mtxParentInverse;

	*/
	m_fnCurve.setCVs( m_pArrPosition );

	MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
	hOutputCurve.setMObject( m_oDataCurve );

	m_isDirtyJointMatrix = false;
	m_isDirtyUpdate = false;

	data.setClean( plug );

	return MS::kSuccess;
}


MStatus sgHair_controledCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aEndJointMatrix )
	{
		m_isDirtyJointMatrix = true;
	}
	else if( plug == aUpdateJoint )
	{
		m_isDirtyUpdate = true;
	}
	else if( plug == aTopJoint )
	{
		m_isDirtyUpdate = true;
	}

	return MS::kSuccess;
}


MStatus sgHair_controledCurve::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnMessageAttribute msgAttr;
	MFnNumericAttribute nAttr;

	aTopJoint = msgAttr.create( "topJoint", "topJoint" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTopJoint ) );

	aEndJointMatrix = mAttr.create( "endJointMatrix", "endJointMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aEndJointMatrix ) );

	aUpdateJoint = nAttr.create( "updateJoint", "updateJoint", MFnNumericData::kBoolean, false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpdateJoint ) );

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aParentInverseMatrix ) );

	aOutputCurve = tAttr.create( "outputCurve", "outCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aEndJointMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpdateJoint, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutputCurve ) );

	return MS::kSuccess;
}