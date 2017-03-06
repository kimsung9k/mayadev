#include "sgHair_attachStartPointCurve.h"

MTypeId  sgHair_attachStartPointCurve::id( 0x20150215 );

MObject  sgHair_attachStartPointCurve::aInputMatrix;
MObject  sgHair_attachStartPointCurve::aInputCurveMatrix;
MObject  sgHair_attachStartPointCurve::aInputCurve;
MObject  sgHair_attachStartPointCurve::aOutputCurve;

void* sgHair_attachStartPointCurve::creator()
{
	return new sgHair_attachStartPointCurve();
}


sgHair_attachStartPointCurve::sgHair_attachStartPointCurve()
{
	m_numCVs = 0;
	m_isDirtyInputMatrix = true;
	m_isDirtyInputCurve = true;
	m_isDirtyInputCurveMatrix = true;
}

sgHair_attachStartPointCurve::~sgHair_attachStartPointCurve()
{
}


MStatus sgHair_attachStartPointCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;
	
	if( m_isDirtyInputCurve || m_isDirtyInputCurveMatrix )
	{
		m_oInputCurve   = data.inputValue( aInputCurve ).asNurbsCurve();
		m_mtxInputCurve = data.inputValue( aInputCurveMatrix ).asMatrix();
		checkAndCreateCurveAndGetPosition();
	}
	if( m_isDirtyInputMatrix || m_isDirtyInputCurveMatrix || m_isDirtyInputCurve )
	{
		m_mtxInput = data.inputValue( aInputMatrix ).asMatrix();
		editPositionByMatrix();
	}
	
	MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
	hOutputCurve.setMObject( m_oOutCurve );

	data.setClean( plug );

	m_isDirtyInputMatrix = false;
	m_isDirtyInputCurve = false;
	m_isDirtyInputCurveMatrix = false;

	return MS::kSuccess;
}


MStatus sgHair_attachStartPointCurve::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMatrix ) );
	aInputCurveMatrix = mAttr.create( "inputCurveMatrix", "inputCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurveMatrix ) );
	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurve ) );
	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurveMatrix, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutputCurve ) );

	return MS::kSuccess;
}


MStatus sgHair_attachStartPointCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMatrix )
		m_isDirtyInputMatrix = true;
	if( plug == aInputCurveMatrix )
		m_isDirtyInputCurveMatrix= true;
	if( plug == aInputCurve )
		m_isDirtyInputCurve = true;

	return MS::kSuccess;
}