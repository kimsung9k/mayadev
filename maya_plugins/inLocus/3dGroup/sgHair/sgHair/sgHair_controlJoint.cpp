#include "sgHair_controlJoint.h"


MTypeId sgHair_controlJoint::id( 0x20150216 );

MObject sgHair_controlJoint::aInputBaseCurve;
MObject sgHair_controlJoint::aInputBaseCurveMatrix;
MObject sgHair_controlJoint::aJointParentBaseMatrix;
MObject sgHair_controlJoint::aStaticRotation;
MObject sgHair_controlJoint::aOutput;
	MObject sgHair_controlJoint::aOutTrans;
		MObject sgHair_controlJoint::aOutTransX;
		MObject sgHair_controlJoint::aOutTransY;
		MObject sgHair_controlJoint::aOutTransZ;
	MObject sgHair_controlJoint::aOutOrient;
		MObject sgHair_controlJoint::aOutOrientX;
		MObject sgHair_controlJoint::aOutOrientY;
		MObject sgHair_controlJoint::aOutOrientZ;

MObject sgHair_controlJoint::aGravityParam;
MObject sgHair_controlJoint::aGravityRange;
MObject sgHair_controlJoint::aGravityWeight;
MObject sgHair_controlJoint::aGravityOffsetMatrix;


void* sgHair_controlJoint::creator()
{
	return new sgHair_controlJoint();
}


sgHair_controlJoint::sgHair_controlJoint()
{
	m_isDirtyMatrix  = true;
	m_isDirtyCurve   = true;
	m_isDirtyOthers = true;
	m_isDirtyGravityOption = true;
	m_isDirtyParentMatrixBase = true;
	m_paramGravity = -1.0;
	m_rangeGravity =  1.0;
}


sgHair_controlJoint::~sgHair_controlJoint()
{

}


MStatus sgHair_controlJoint::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle   hStaticRotation = data.inputValue( aStaticRotation );
	m_bStaticRotation = hStaticRotation.asBool();

	if( m_isDirtyMatrix )
	{
		MDataHandle hInputBaseCurveMatrix = data.inputValue( aInputBaseCurveMatrix );
		m_mtxBaseCurve       = hInputBaseCurveMatrix.asMatrix(); 
	}
	if( m_isDirtyParentMatrixBase )
	{
		MDataHandle hJointParenBasetMatrix = data.inputValue( aJointParentBaseMatrix );
		m_mtxJointParentBase = hJointParenBasetMatrix.asMatrix();
	}
	if( m_isDirtyCurve || m_isDirtyParentMatrixBase )
	{
		MDataHandle hInputBaseCurve = data.inputValue( aInputBaseCurve );
		MFnNurbsCurve fnCurve = hInputBaseCurve.asNurbsCurve();
		fnCurve.getCVs( m_cvs );
		getJointPositionBaseWorld();
	}
	if( m_isDirtyGravityOption || m_isDirtyCurve || m_isDirtyParentMatrixBase )
	{
		MDataHandle hGravityParam  = data.inputValue( aGravityParam );
		MDataHandle hGravityRange  = data.inputValue( aGravityRange );
		MDataHandle hGravityWeight = data.inputValue( aGravityWeight );
		MDataHandle hGravityOffsetMatrix = data.inputValue( aGravityOffsetMatrix );

		m_paramGravity = hGravityParam.asDouble();
		m_rangeGravity = hGravityRange.asDouble();
		m_weightGravity = hGravityWeight.asDouble();
		m_mtxGravityOffset = hGravityOffsetMatrix.asMatrix();
		m_mtxGravityOffset( 3,0 ) = 0.0;
		m_mtxGravityOffset( 3,1 ) = 0.0;
		m_mtxGravityOffset( 3,2 ) = 0.0;
		setGravityJointPositionWorld();
	}

	setOutput();

	MArrayDataHandle  hArrOutput = data.outputValue( aOutput );
	MArrayDataBuilder builderOutput( aOutput, m_cvs.length() );

	for( int i=0; i< m_cvs.length(); i++ )
	{
		MDataHandle hOutput = builderOutput.addElement( i );
		MDataHandle hOutTrans = hOutput.child( aOutTrans );
		MDataHandle hOutOrient = hOutput.child( aOutOrient );

		hOutTrans.set( m_vectorArrTransJoint[i] );
		hOutOrient.set( m_vectorArrRotateJoint[i] );
	}

	hArrOutput.set( builderOutput );
	hArrOutput.setAllClean();

	data.setClean( plug );

	m_isDirtyMatrix  = false;
	m_isDirtyCurve   = false;
	m_isDirtyGravityOption = false;
	m_isDirtyParentMatrixBase = false;

	return MS::kSuccess;
}


MStatus sgHair_controlJoint::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aJointParentBaseMatrix )
	{
		m_isDirtyParentMatrixBase = true;
	}
	if( plug == aInputBaseCurveMatrix )
	{
		m_isDirtyMatrix = true;
	}
	else if( plug == aInputBaseCurve )
	{
		m_isDirtyCurve = true;
	}
	else if( plug == aGravityParam || plug == aGravityRange || plug == aGravityWeight
		|| plug == aGravityOffsetMatrix )
	{
		m_isDirtyGravityOption = true;
	}
	else if( plug == aStaticRotation )
	{
		m_isDirtyParentMatrixBase = true;
		m_isDirtyMatrix = true;
		m_isDirtyCurve = true;
		m_isDirtyGravityOption = true;
	}
	return MS::kSuccess;
}


MStatus sgHair_controlJoint::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnMessageAttribute msgAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;

	aInputBaseCurve = tAttr.create( "inputBaseCurve", "inputBaseCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputBaseCurve ) );

	aInputBaseCurveMatrix = mAttr.create( "inputBaseCurveMatrix", "inputBaseCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputBaseCurveMatrix ) );

	aJointParentBaseMatrix = mAttr.create( "jointParentBaseMatrix", "jointParentBaseMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aJointParentBaseMatrix ) );

	aGravityParam  = nAttr.create( "gravityParam", "gravityParam", MFnNumericData::kDouble, 0.0 );
	nAttr.setMin( 0.0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGravityParam ) );
	aGravityRange  = nAttr.create( "gravityRange", "gravityRange", MFnNumericData::kDouble, 0.0 );
	nAttr.setMin( 0.0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGravityRange ) );
	aGravityWeight  = nAttr.create( "gravityWeight", "gravityWeight", MFnNumericData::kDouble, 0.0 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGravityWeight ) );
	aGravityOffsetMatrix = mAttr.create( "gravityOffsetMatrix", "gravityOffsetMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGravityOffsetMatrix ) );

	aStaticRotation = nAttr.create( "staticRotation", "staticRotation", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aStaticRotation ) );

	aOutput  = cAttr.create( "output", "output" );

	aOutTransX = nAttr.create( "outTransX", "otx", MFnNumericData::kDouble );
	aOutTransY = nAttr.create( "outTransY", "oty", MFnNumericData::kDouble );
	aOutTransZ = nAttr.create( "outTransZ", "otz", MFnNumericData::kDouble );
	aOutTrans  = nAttr.create( "outTrans", "ot", aOutTransX, aOutTransY, aOutTransZ );

	aOutOrientX = uAttr.create( "outRotateX", "orx", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrientY = uAttr.create( "outRotateY", "ory", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrientZ = uAttr.create( "outRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrient  = nAttr.create( "outRotate", "outRotate", aOutOrientX, aOutOrientY, aOutOrientZ );

	cAttr.addChild( aOutTrans );
	cAttr.addChild( aOutOrient );
	cAttr.setStorable( false );
	cAttr.setArray( true );
	cAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutput ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGravityParam,  aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGravityRange,  aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGravityWeight, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aJointParentBaseMatrix, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGravityOffsetMatrix, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputBaseCurve, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputBaseCurveMatrix, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aStaticRotation, aOutput ) );

	return MS::kSuccess;
}