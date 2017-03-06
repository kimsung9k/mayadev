#include "sgQubicle.h"


MTypeId sgQubicle::id( 0x2015091400 );

MObject sgQubicle::aInputMesh;
MObject sgQubicle::aInputMeshMatrix;
MObject sgQubicle::aPointDetail;
MObject sgQubicle::aOutputMesh;


void* sgQubicle::creator()
{
	return new sgQubicle();
}


sgQubicle::sgQubicle()
{
}


sgQubicle::~sgQubicle()
{
}


MStatus sgQubicle::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hInputMesh = data.inputValue( aInputMesh );
	MObject oInputMesh = hInputMesh.asMesh();
	MDataHandle hPointDetail = data.inputValue( aPointDetail );
	float pointDetail = hPointDetail.asFloat();


	MMeshIntersector meshIntersector;
	meshIntersector.create( oInputMesh );


	MFnDagNode dagNodeMesh = oInputMesh;
	MBoundingBox bb = dagNodeMesh.boundingBox();


	MDataHandle hOutputMesh = data.outputValue( aOutputMesh );

	return MS::kSuccess;
}


MStatus sgQubicle::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute   tAttr;
	MFnCompoundAttribute cAttr;
	MFnMatrixAttribute mAttr;

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );

	aInputMeshMatrix = mAttr.create( "inputMeshMatrix", "inputMeshMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshMatrix ) );

	aPointDetail = nAttr.create( "pointDetail", "pointDetail", MFnNumericData::kFloat, 1 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPointDetail ) );

	aOutputMesh = tAttr.create( "outputMesh", "outputMesh", MFnData::kMesh );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMesh ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutputMesh ) );

	return MS::kSuccess;
}


MStatus sgQubicle::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	return MS::kSuccess;
}