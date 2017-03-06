#include "matrixFromPolygon.h"
#include "matrixFromPolygon_def.h"

MTypeId   matrixFromPolygon::id( 0xc8d306 );

MObject   matrixFromPolygon::aInputMesh;
MObject   matrixFromPolygon::aInputMeshMatrix;
MObject   matrixFromPolygon::aPolygonIndex;
MObject   matrixFromPolygon::aU;
MObject   matrixFromPolygon::aV;
MObject   matrixFromPolygon::aOutputMatrix;


matrixFromPolygon::matrixFromPolygon(){}
matrixFromPolygon::~matrixFromPolygon(){}

void*  matrixFromPolygon::creator()
{
	return new matrixFromPolygon();
}

MStatus  matrixFromPolygon::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	//MFnDependencyNode thisNode( thisMObject() );
	//cout << thisNode.name() << ", start" << endl;

	if( plug == aOutputMatrix )
	{
		MDataHandle  hInputMesh = data.inputValue( aInputMesh, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MDataHandle  hInputMeshMatrix = data.inputValue( aInputMeshMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MDataHandle  hPolygonIndex = data.inputValue( aPolygonIndex, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MDataHandle  hU = data.inputValue( aU, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MDataHandle  hV = data.inputValue( aV, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		MDataHandle  hOutputMatrix = data.outputValue( aOutputMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		MMatrix outMatrix;
		getMatrixByPoints( outMatrix, hPolygonIndex.asInt(), hU.asDouble(), hV.asDouble(), hInputMesh.asMesh() );

		outMatrix *= hInputMeshMatrix.asMatrix();

		hOutputMatrix.set( outMatrix );

		data.setClean( plug );
	}
	//cout << thisNode.name() << ", end" << endl;

	return MS::kSuccess;
}

MStatus  matrixFromPolygon::initialize()
{
	MStatus  status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute  mAttr;
	MFnTypedAttribute   tAttr;

	aOutputMatrix = mAttr.create( "outputMatrix", "outputMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMatrix ) );

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutputMatrix ) );

	aInputMeshMatrix = mAttr.create( "inputMeshMatrix", "inputMeshMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutputMatrix ) );

	aPolygonIndex = nAttr.create( "polygonIndex", "polygonIndex", MFnNumericData::kInt, 0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPolygonIndex ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPolygonIndex, aOutputMatrix ) );

	aU = nAttr.create( "u", "u", MFnNumericData::kDouble, 0.5 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aU ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aU, aOutputMatrix ) );

	aV = nAttr.create( "v", "v", MFnNumericData::kDouble, 0.5 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aV ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aV, aOutputMatrix ) );

	return  MS::kSuccess;
}