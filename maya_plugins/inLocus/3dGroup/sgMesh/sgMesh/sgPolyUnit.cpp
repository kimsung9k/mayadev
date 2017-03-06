#include "sgPolyUnit.h"


MTypeId sgPolyUnit::id( 0x2015061500 );

MObject sgPolyUnit::aInputMeshs;
MObject sgPolyUnit::aOutputMesh;


void* sgPolyUnit::creator()
{
	return new sgPolyUnit();
}


sgPolyUnit::sgPolyUnit()
{
	m_isDirty_inputMeshs = true;
	m_oArr_inputMesh.clear();
}


sgPolyUnit::~sgPolyUnit()
{
}


MStatus sgPolyUnit::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	check_and_buildMeshData( data );

	MDataHandle hOutputMesh = data.outputValue( aOutputMesh );
	hOutputMesh.set( m_sgBuildMeshData.m_oMesh );

	m_isDirty_inputMeshs = false;
	m_rebuildMeshData = false;

	return MS::kSuccess;
}



MStatus sgPolyUnit::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute   tAttr;
	MFnCompoundAttribute cAttr;

	aInputMeshs = tAttr.create( "inputMeshs", "inputMeshs", MFnData::kMesh );
	tAttr.setStorable( true );
	tAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshs ) );

	aOutputMesh = tAttr.create( "outputMesh", "outputMesh", MFnData::kMesh );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMesh ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshs, aOutputMesh ) );

	return MS::kSuccess;
}



MStatus sgPolyUnit::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMeshs )
	{
		m_isDirty_inputMeshs = true;
	}

	return MS::kSuccess;
}