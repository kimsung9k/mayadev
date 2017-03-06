#include "meshVtxAttachPointNode.h"


MTypeId		MeshVtxAttachPointNode::id( 0x2014042000 );


MObject     MeshVtxAttachPointNode::aOutPoint;
	MObject     MeshVtxAttachPointNode::aOutPointX;
	MObject     MeshVtxAttachPointNode::aOutPointY;
	MObject     MeshVtxAttachPointNode::aOutPointZ;

MObject     MeshVtxAttachPointNode::aBaseMesh;
MObject		MeshVtxAttachPointNode::aPointInfo;
	MObject		MeshVtxAttachPointNode::aVtxIndex;
	MObject		MeshVtxAttachPointNode::aNormalDistance;
	MObject		MeshVtxAttachPointNode::aMultWidthBBS;


MeshVtxAttachPointNode::MeshVtxAttachPointNode()
{
}

MeshVtxAttachPointNode::~MeshVtxAttachPointNode()
{
}


void* MeshVtxAttachPointNode::creator()
{
	return new MeshVtxAttachPointNode();
}



MStatus MeshVtxAttachPointNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hBaseMesh = data.inputValue( aBaseMesh );

	MArrayDataHandle hArrPointInfo = data.inputArrayValue( aPointInfo );

	return MS::kSuccess;
}




MStatus	MeshVtxAttachPointNode::initialize()
{
	MStatus status;
	
	MFnTypedAttribute	 tAttr;
	MFnNumericAttribute  nAttr;
	MFnCompoundAttribute cAttr;

	aOutPointX  = nAttr.create( "outPointX", "outPointX", MFnNumericData::kDouble, 0.0 );
	aOutPointY  = nAttr.create( "outPointY", "outPointY", MFnNumericData::kDouble, 0.0 );
	aOutPointZ  = nAttr.create( "outPointZ", "outPointZ", MFnNumericData::kDouble, 0.0 );
	aOutPoint   = nAttr.create( "outPoint", "outPoint", aOutPointX, aOutPointY, aOutPointZ );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutPoint ) );

	aBaseMesh   = tAttr.create( "baseMesh", "baseMesh", MFnData::kMesh );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMesh ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMesh, aOutPoint ) );

	aPointInfo  = cAttr.create( "pointInfo", "pointInfo" );

	aVtxIndex = nAttr.create( "vtxIndex", "vtxIndex", MFnNumericData::kInt, 0 );
	nAttr.setArray( true );
	aNormalDistance = nAttr.create( "normalDistance", "normalDistance", MFnNumericData::kDouble, 0.0 );
	aMultWidthBBS   = nAttr.create( "multWidthBBS", "multWidthBBS", MFnNumericData::kBoolean, true );

	cAttr.addChild( aVtxIndex );
	cAttr.addChild( aNormalDistance );
	cAttr.addChild( aMultWidthBBS );

	cAttr.setStorable( true );
	cAttr.setArray( true );

	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPointInfo ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPointInfo, aOutPoint ) );

	return MS::kSuccess;
}


MStatus MeshVtxAttachPointNode::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aVtxIndex )
	{
		
	}

	return MS::kSuccess;
}