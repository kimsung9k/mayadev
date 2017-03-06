#include "node.h"

MObject MainNode::aMsgSkinCluster;
MObject MainNode::aDeltaInfo;
	MObject MainNode::aDeltaName;
	MObject MainNode::aInputMesh;
	MObject MainNode::aDelta;
		MObject MainNode::aDeltaX;
		MObject MainNode::aDeltaY;
		MObject MainNode::aDeltaZ;
	MObject MainNode::aWeight;

MTypeId MainNode::id( 0xeeee01 );


MainNode::MainNode()
{
	m_updateInputGeom = true;
	m_numDeltaInfo = 0;
	m_numBeforeDeltaInfo = 0;
}


MainNode::~MainNode()
{
}


void* MainNode::creator()
{
	return new MainNode();
}


MStatus  MainNode::deform( MDataBlock& data, MItGeometry& itGeo,
	                       const MMatrix& mat, unsigned int multiIndex )
{
	MStatus status;

	if( data.inputValue( envelope ).asFloat() < 0.001 )
	{
		return MS::kSuccess;
	}

	m_plugDeltaInfo = MFnDependencyNode( thisMObject() ).findPlug( aDeltaInfo );
	
	MArrayDataHandle hArrDeltaInfo = data.inputArrayValue( aDeltaInfo );
	status = chk_updateSkinClusterInfo( mat );
	if( !status ) return MS::kSuccess;
	
	chk_inputGeomPoints( itGeo );
	
	chk_deltaInfoAllUpdate( hArrDeltaInfo, mat );
	
	hArrDeltaInfo = data.inputArrayValue( aDeltaInfo );
	chk_deltaInfoMovedUpdate( hArrDeltaInfo, mat );
	
	hArrDeltaInfo = data.inputArrayValue( aDeltaInfo );
	chk_updateWeights( hArrDeltaInfo );

	caculate();

	itGeo.setAllPositions( m_pointArrResult );

	return MS::kSuccess;
}


MStatus MainNode::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMesh )
	{
		MPlug plugParent = plug.parent( &status );
		m_indicesUpdateMesh.append( plugParent.logicalIndex() );
	}
	else if( plug == inputGeom )
	{
		m_updateInputGeom = true;
	}
	else if( plug == aWeight )
	{
		MPlug plugParent = plug.parent( &status );
		m_weightUpdateIndices.append( plugParent.logicalIndex() );
	}

	return MS::kSuccess;
}


MStatus MainNode::initialize()
{
	MStatus status;

	MFnMessageAttribute  msgAttr;

	MFnCompoundAttribute cAttr;
	MFnTypedAttribute    tAttr;
	MFnNumericAttribute  nAttr;

	
	aMsgSkinCluster = msgAttr.create( "skinCluster", "skinCluster" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMsgSkinCluster ) );

	aDeltaInfo = cAttr.create( "deltaInfo", "deltaInfo" );
	
	aDeltaName = tAttr.create( "deltaName", "deltaName", MFnData::kString );

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	tAttr.setCached( false );
	tAttr.setStorable( false );
	
	aDeltaX = nAttr.create( "deltaX", "deltaX", MFnNumericData::kDouble );
	aDeltaY = nAttr.create( "deltaY", "deltaY", MFnNumericData::kDouble );
	aDeltaZ = nAttr.create( "deltaZ", "deltaZ", MFnNumericData::kDouble );
	aDelta  = nAttr.create( "delta", "delta", aDeltaX, aDeltaY, aDeltaZ );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );

	aWeight = nAttr.create( "weight", "weight", MFnNumericData::kFloat, 1.0 );
	nAttr.setKeyable( true );

	cAttr.addChild( aDeltaName );
	cAttr.addChild( aInputMesh );
	cAttr.addChild( aDelta );
	cAttr.addChild( aWeight );
	cAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aDeltaInfo ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aDeltaInfo, outputGeom ) );


	return MS::kSuccess;
}