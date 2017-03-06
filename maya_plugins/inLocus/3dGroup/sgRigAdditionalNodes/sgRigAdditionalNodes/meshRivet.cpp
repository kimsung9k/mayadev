#include "meshRivet.h"

MTypeId meshRivet::id( 0x2014062600 );

MObject meshRivet::aInputMesh;
MObject meshRivet::aMeshMatrix;
MObject meshRivet::aCenterIndices;
MObject meshRivet::aAimPivIndices;
MObject meshRivet::aAimIndices;
MObject meshRivet::aUpPivIndices;
MObject meshRivet::aUpIndices;
MObject meshRivet::aAimAxis;
MObject meshRivet::aUpAxis;
MObject meshRivet::aInverseCross;

MObject meshRivet::aParentInverseMatrix;

MObject meshRivet::aResult;
MObject meshRivet::aOutMatrix;
MObject meshRivet::aOutTranslate;
	MObject meshRivet::aOutTranslateX;
	MObject meshRivet::aOutTranslateY;
	MObject meshRivet::aOutTranslateZ;
MObject meshRivet::aOutRotate;
	MObject meshRivet::aOutRotateX;
	MObject meshRivet::aOutRotateY;
	MObject meshRivet::aOutRotateZ;

meshRivet::meshRivet()
{
	m_dirty = true;
	m_meshDirty = true;
	m_matrixDirty = true;
	m_parentInverseDirty = true;
	m_indicesCenterDirty = true;
	m_indicesAimDirty = true;
	m_indicesUpDirty = true;
}

meshRivet::~meshRivet()
{
}


void* meshRivet::creator()
{
	return new meshRivet();
}


MStatus meshRivet::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	if( !m_dirty ) return setResult( plug, data );

	if( m_meshDirty )
	{
		getMeshInfomation( data );
	}
	if( m_matrixDirty )
	{
		getMeshMatrix( data );
	}
	if( m_parentInverseDirty )
	{
		getParentInverseMatrix( data );
	}
	if( m_indicesCenterDirty )
	{
		getCenterIndices( data );
	}
	if( m_indicesAimDirty )
	{
		getAimIndices( data );
	}
	if( m_indicesUpDirty )
	{
		getUpIndices( data );
	}

	m_aimAxis = data.inputValue( aAimAxis ).asUChar();
	m_upAxis  = data.inputValue( aUpAxis ).asUChar();

	setResult( plug, data );
	m_dirty = false;

	return MS::kSuccess;
}


MStatus meshRivet::initialize()
{
	MStatus status;

	MFnCompoundAttribute cAttr;
	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MFnUnitAttribute     uAttr;
	MFnEnumAttribute     eAttr;
	MFnTypedAttribute    tAttr;

	aResult = cAttr.create( "result", "result" );

	aOutMatrix = mAttr.create( "outMatrix", "outMatrix" );

	aOutTranslateX = nAttr.create( "outTranslateX", "otx", MFnNumericData::kDouble, 0.0 );
	aOutTranslateY = nAttr.create( "outTranslateY", "oty", MFnNumericData::kDouble, 0.0 );
	aOutTranslateZ = nAttr.create( "outTranslateZ", "otz", MFnNumericData::kDouble, 0.0 );
	aOutTranslate  = nAttr.create( "outTranslate", "ot", aOutTranslateX, aOutTranslateY, aOutTranslateZ, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aOutRotateX = uAttr.create( "outRotateX", "orx", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotateY = uAttr.create( "outRotateY", "ory", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotateZ = uAttr.create( "outRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0 );
	aOutRotate  = nAttr.create( "outRotate", "or",  aOutRotateX, aOutRotateY, aOutRotateZ );

	cAttr.addChild( aOutMatrix );
	cAttr.addChild( aOutTranslate );
	cAttr.addChild( aOutRotate );
	cAttr.setStorable( false );

	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aResult ) );

	aInputMesh = tAttr.create( "inputMesh", "inMesh", MFnData::kMesh );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aResult ) );

	aMeshMatrix = mAttr.create( "meshMatrix", "meshMtx" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMeshMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMeshMatrix, aResult ) );

	aCenterIndices = nAttr.create( "centerIndices", "cnids", MFnNumericData::kInt );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCenterIndices ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCenterIndices, aResult ) );

	aAimPivIndices = nAttr.create( "aimPivIndices", "aimPivIds", MFnNumericData::kInt );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimPivIndices ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimPivIndices, aResult ) );

	aAimIndices = nAttr.create( "aimIndices", "aimids", MFnNumericData::kInt );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimIndices ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimIndices, aResult ) );

	aUpPivIndices  = nAttr.create( "upPivIndices", "upPivIds", MFnNumericData::kInt );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpPivIndices ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpPivIndices, aResult ) );

	aUpIndices  = nAttr.create( "upIndices", "upids", MFnNumericData::kInt );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpIndices ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpIndices, aResult ) );

	aAimAxis = eAttr.create( "aimAxis", "aimax");
	eAttr.addField( "X", 0 );
	eAttr.addField( "Y", 1 );
	eAttr.addField( "Z", 2 );
	eAttr.addField( "-X", 3 );
	eAttr.addField( "-Y", 4 );
	eAttr.addField( "-Z", 5 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimAxis ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimAxis, aResult ) );

	aUpAxis = eAttr.create( "upAxis", "upax", 1 );
	eAttr.addField( "X", 0 );
	eAttr.addField( "Y", 1 );
	eAttr.addField( "Z", 2 );
	eAttr.addField( "-X", 3 );
	eAttr.addField( "-Y", 4 );
	eAttr.addField( "-Z", 5 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpAxis ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpAxis, aResult ) );

	aInverseCross = nAttr.create( "inverseCross", "invc", MFnNumericData::kBoolean, false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInverseCross ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInverseCross, aResult ) );

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aParentInverseMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aResult ) );

	return MS::kSuccess;
}


MStatus meshRivet::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMesh )
	{
		m_meshDirty = true;
	}

	if( plug == aMeshMatrix )
	{
		m_matrixDirty = true;
	}

	if( plug == aParentInverseMatrix )
	{
		m_parentInverseDirty = true;
	}

	if( plug == aCenterIndices )
	{
		m_indicesCenterDirty = true;
	}
	if( plug == aAimIndices || plug == aAimPivIndices )
	{
		m_indicesAimDirty = true;
	}
	if( plug == aUpIndices || plug == aUpPivIndices )
	{
		m_indicesUpDirty = true;
	}
	m_dirty = true;

	return MS::kSuccess;
}