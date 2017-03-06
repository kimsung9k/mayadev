#include "aimObjectMatrix.h"

MTypeId     aimObjectMatrix::id( 0x2014051300 );

MObject     aimObjectMatrix::aBaseMatrix;
MObject     aimObjectMatrix::aTargetMatrix;
MObject     aimObjectMatrix::aParentInverseMatrix;
MObject     aimObjectMatrix::aOffset;
	MObject     aimObjectMatrix::aOffsetX;
	MObject     aimObjectMatrix::aOffsetY;
	MObject     aimObjectMatrix::aOffsetZ;
MObject     aimObjectMatrix::aOutMatrix;
MObject     aimObjectMatrix::aOutRotate;
	MObject     aimObjectMatrix::aOutRotateX;
	MObject     aimObjectMatrix::aOutRotateY;
	MObject     aimObjectMatrix::aOutRotateZ;
MObject     aimObjectMatrix::aOutTranslate;
	MObject     aimObjectMatrix::aOutTranslateX;
	MObject     aimObjectMatrix::aOutTranslateY;
	MObject     aimObjectMatrix::aOutTranslateZ;
MObject    aimObjectMatrix::aAimAxis;
MObject    aimObjectMatrix::aInverseAim;
MObject    aimObjectMatrix::aWorldSpaceOutput;
MObject    aimObjectMatrix::aByCurve;
MObject    aimObjectMatrix::aInputCurve;
MObject    aimObjectMatrix::aCurveMatrix;


aimObjectMatrix::aimObjectMatrix()
{
	m_bBaseCurveModified = true;
	m_bCurveMatrixModified = true;
	m_isOffsetDirty = true;
}

aimObjectMatrix::~aimObjectMatrix(){}


void* aimObjectMatrix::creator()
{
	return new aimObjectMatrix();
}


MStatus aimObjectMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	m_mtxTarget = data.inputValue( aTargetMatrix ).asMatrix();
	m_mtxBase = data.inputValue( aBaseMatrix ).asMatrix();
	m_aimIndex = data.inputValue( aAimAxis ).asUChar();
	m_upIndex  = m_aimIndex + 1;
	m_inverseAim = data.inputValue( aInverseAim ).asBool();
	
	bool byCurve = data.inputValue( aByCurve ).asBool();
	bool worldSpaceOutput = data.inputValue( aWorldSpaceOutput ).asBool();

	if( m_isOffsetDirty )
	{
		MDataHandle hOffset = data.inputValue( aOffset );
		MDataHandle hOffsetX = hOffset.child( aOffsetX );
		MDataHandle hOffsetY = hOffset.child( aOffsetY );
		MDataHandle hOffsetZ = hOffset.child( aOffsetZ );

		double rotX = hOffsetX.asDouble();
		double rotY = hOffsetY.asDouble();
		double rotZ = hOffsetZ.asDouble();

		MTransformationMatrix trMtx;

		double inputRotate[3] ={ rotX, rotY, rotZ };
		trMtx.setRotation( inputRotate, MTransformationMatrix::kXYZ, MSpace::kTransform );

		m_mtxOffset = trMtx.asMatrix();
	}

	if( byCurve )
	{
		if( m_bBaseCurveModified )
		{
			m_fnCurve.setObject( data.inputValue( aInputCurve ).asNurbsCurve() );
			m_bBaseCurveModified = false;
		}
		if( m_bCurveMatrixModified )
		{
			m_mtxCurve = data.inputValue( aCurveMatrix ).asMatrix();
			m_bCurveMatrixModified = false;
		}
		getMatrixByCurve();
	}
	caculate();

	if( worldSpaceOutput )
	{
		MMatrix mtxParentInverse = data.inputValue( aParentInverseMatrix ).asMatrix();
		m_mtxOutput = m_mtxOffset * m_mtxOutput * m_mtxBase * mtxParentInverse;
		m_mtxTransform = m_mtxOutput;
	}
	else
	{
		m_mtxOutput = m_mtxOffset * m_mtxOutput;
		m_mtxTransform = m_mtxOutput;
	}

	MDataHandle hOutMatrix = data.outputValue( aOutMatrix );
	hOutMatrix.set( m_mtxOutput );

	MTransformationMatrix trMtx( m_mtxTransform );
	MDataHandle hOutRotate = data.outputValue( aOutRotate );
	hOutRotate.set( trMtx.eulerRotation().asVector() );

	if( worldSpaceOutput )
	{
		MDataHandle hOutTranslate = data.outputValue( aOutTranslate );
		hOutTranslate.set( trMtx.translation( MSpace::kTransform ) );
	}

	return MS::kSuccess;
}


MStatus aimObjectMatrix::initialize()
{
	MStatus status;

	MFnTypedAttribute   tAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute    uAttr;
	MFnMatrixAttribute  mAttr;
	MFnEnumAttribute    eAttr;

	aOutMatrix = mAttr.create( "outMatrix", "outMatrix" );
	mAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutMatrix ) );

	aOutRotateX = uAttr.create( "outRotateX", "outRotateX", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotateY = uAttr.create( "outRotateY", "outRotateY", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotateZ = uAttr.create( "outRotateZ", "outRotateZ", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotate  = nAttr.create( "outRotate", "outRotate", aOutRotateX, aOutRotateY, aOutRotateZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutRotate ) );

	aOutTranslateX = nAttr.create( "outTranslateX", "outTranslateX", MFnNumericData::kDouble, 0.0 );
	aOutTranslateY = nAttr.create( "outTranslateY", "outTranslateY", MFnNumericData::kDouble, 0.0 );
	aOutTranslateZ = nAttr.create( "outTranslateZ", "outTranslateZ", MFnNumericData::kDouble, 0.0 );
	aOutTranslate  = nAttr.create( "outTranslate", "outTranslate", aOutTranslateX, aOutTranslateY, aOutTranslateZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutTranslate ) );

	aBaseMatrix = mAttr.create( "baseMatrix", "baseMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMatrix, aOutTranslate ) );

	aTargetMatrix = mAttr.create( "targetMatrix", "targetMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTargetMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTargetMatrix, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTargetMatrix, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTargetMatrix, aOutTranslate ) );

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "parentInverseMatrix" );
	mAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aParentInverseMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutTranslate ) );

	aOffsetX = uAttr.create( "offsetX", "offsetX", MFnUnitAttribute::kAngle, 0.0 );
	aOffsetY = uAttr.create( "offsetY", "offsetY", MFnUnitAttribute::kAngle, 0.0 );
	aOffsetZ = uAttr.create( "offsetZ", "offsetZ", MFnUnitAttribute::kAngle, 0.0 );
	aOffset  = nAttr.create( "offset", "offset", aOffsetX, aOffsetY, aOffsetZ );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOffset ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aOffset, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aOffset, aOutRotate ) );

	aAimAxis = eAttr.create( "aimAxis", "aimAxis" );
	eAttr.addField( " X", 0 );eAttr.addField( " Y", 1 );eAttr.addField( " Z", 2 );
	eAttr.addField( "-X", 3 );eAttr.addField( "-Y", 4 );eAttr.addField( "-Z", 5 );
	eAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimAxis ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimAxis, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimAxis, aOutRotate ) );

	aInverseAim = nAttr.create( "inverseAim", "inverseAim", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInverseAim ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInverseAim, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInverseAim, aOutRotate ) );

	aWorldSpaceOutput = nAttr.create( "worldSpaceOutput", "worldSpaceOutput", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aWorldSpaceOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWorldSpaceOutput, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWorldSpaceOutput, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aWorldSpaceOutput, aOutTranslate ) );

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutTranslate ) );

	aByCurve = nAttr.create("byCurve", "byCurve", MFnNumericData::kBoolean, false );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aByCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aByCurve, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aByCurve, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aByCurve, aOutTranslate ) );

	aCurveMatrix = mAttr.create( "curveMatrix", "curveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCurveMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCurveMatrix, aOutMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCurveMatrix, aOutRotate ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCurveMatrix, aOutTranslate ) );

	return MS::kSuccess;
}


MStatus aimObjectMatrix::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputCurve )
	{
		m_bBaseCurveModified = true;
	}

	if( plug == aCurveMatrix )
	{
		m_bCurveMatrixModified = true;
	}

	if( plug == aOffset || plug == aOffsetX || plug == aOffsetY || plug == aOffsetZ )
	{
		m_isOffsetDirty = true;
	}

	return MS::kSuccess;
}