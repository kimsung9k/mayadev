#include "addMirrorBlendMeshInfos.h"
#include "blendAndFixedShape.h"
#include "blendAndFixedShape_def.h"


MTypeId     blendAndFixedShape::id( 0xc8d603 );

MObject     blendAndFixedShape::aDriverWeights;
MObject     blendAndFixedShape::aMinusWeightEnable;

MObject     blendAndFixedShape::aBlendMeshInfos;
	MObject     blendAndFixedShape::aInputMesh;
	MObject     blendAndFixedShape::aDeltas;
		MObject     blendAndFixedShape::aDeltaX;
		MObject     blendAndFixedShape::aDeltaY;
		MObject     blendAndFixedShape::aDeltaZ;
	MObject     blendAndFixedShape::aTargetWeights;
	MObject     blendAndFixedShape::aMeshName;
	MObject		blendAndFixedShape::aKeepMatrix;
	MObject		blendAndFixedShape::aAnimCurve;
	MObject		blendAndFixedShape::aAnimCurveOutput;

MObject    blendAndFixedShape::aUpdateMeshData;


blendAndFixedShape::blendAndFixedShape()
{
	MThreadPool::init();
	blendMeshUpdated = false;
	pTaskData   = new blendAndFixedShape_taskData;
	pThreadData = new blendAndFixedShape_threadData;

	beforeBlendMeshNum = 0;
	updateBlendMeshIndices.clear();
	updateDeltaIndices.clear();
	createMirrorIndex = -1;

}


blendAndFixedShape::~blendAndFixedShape() 
{
	MThreadPool::release();
	delete pTaskData;
	delete pThreadData;
}


MStatus blendAndFixedShape::deform( MDataBlock& data,
									   MItGeometry& itGeo,
									   const MMatrix& localToWorldMatrix,
									   unsigned int geomIndex )
{
	MStatus status;
	MArrayDataHandle  hArrBlendMeshInfos = data.inputArrayValue( aBlendMeshInfos );
	MArrayDataHandle  hArrDriverWeights  = data.inputArrayValue( aDriverWeights );
	MDataHandle       hMinusWeightEnable = data.inputValue( aMinusWeightEnable );

	MDataHandle hEnvelop = data.inputValue( envelope );
	envValue = hEnvelop.asFloat();

	if( !envValue ) return MS::kSuccess;

	if( !blendMeshUpdated )
	{
		itGeo.allPositions( pTaskData->basePoints );
		pTaskData->movedPoints.setLength( pTaskData->basePoints.length() );
		blendMeshUpdated = true;
	}

	updateDeltaIndices.clear();
	status = meshPoints_To_DeltaAttrs( hArrBlendMeshInfos );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	deltaAttrs_To_Task( hArrBlendMeshInfos );

	weightAttrs_To_task( hArrBlendMeshInfos );
	currentWeights_To_task( hArrDriverWeights );

	separateSameChannelIndices();
	setOverIndicesArray( hArrBlendMeshInfos );
	getBlendMeshWeight();
	shareWeightBySameChannel();

	status = setBlendMeshWeightByAnimCurve();
	CHECK_MSTATUS_AND_RETURN_IT( status );

	//setOverWeights();
	setEnvWeights();
	setWeightedBlendIndices();
	//cout << "weighted indices : " << pTaskData->weightedIndices << endl;
	//cout << "delta length : " << pTaskData->deltas.size() << endl;
	//cout << "blendWeight : " << pTaskData->blendMeshWeights << endl;
	setThread();
	MThreadPool::newParallelRegion( parallelCompute, pThreadData );
	endThread();

	itGeo.setAllPositions( pTaskData->movedPoints );

	finishCaculation();

	updateBlendMeshIndices.clear();
	updateDeltaIndices.clear();
	return MS::kSuccess;
}


void  blendAndFixedShape::finishCaculation()
{
	updateBlendMeshIndices.clear();
}


void* blendAndFixedShape::creator()
{
	return new blendAndFixedShape();
}


MStatus blendAndFixedShape::initialize()	
{
	MStatus   status;

	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnMessageAttribute msgAttr;

	aDriverWeights = nAttr.create( "driverWeights", "driverWeights", MFnNumericData::kFloat, 0.0f );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aDriverWeights ) );

	aMinusWeightEnable = nAttr.create( "minusWeightEnable" , "minusWeightEnable", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMinusWeightEnable ) );

	aBlendMeshInfos = cAttr.create( "blendMeshInfos", "blendMeshInfos" );
	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	tAttr.setStorable( false );
	tAttr.setCached( false );
	aDeltaX = nAttr.create( "deltaX", "deltaX", MFnNumericData::kDouble );
	aDeltaY = nAttr.create( "deltaY", "deltaY", MFnNumericData::kDouble );
	aDeltaZ = nAttr.create( "deltaZ", "deltaZ", MFnNumericData::kDouble );
	aDeltas = nAttr.create( "deltas", "deltas", aDeltaX, aDeltaY, aDeltaZ );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( true );
	aTargetWeights = nAttr.create( "targetWeights", "targetWeights", MFnNumericData::kFloat );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( true );
	aMeshName = tAttr.create( "meshName", "meshName", MFnData::kString );
	tAttr.setStorable( true );
	aKeepMatrix = mAttr.create( "keepMatrix", "keepMatrix" );
	mAttr.setStorable( true );
	mAttr.setArray( true );
	aAnimCurve = msgAttr.create( "animCurve", "animCurve" );
	msgAttr.setStorable( false );
	aAnimCurveOutput = nAttr.create( "animCurveOutput", "animCurveOutput", MFnNumericData::kDouble );
	nAttr.setStorable( false );

	cAttr.addChild( aInputMesh );
	cAttr.addChild( aDeltas );
	cAttr.addChild( aTargetWeights );
	cAttr.addChild( aMeshName );
	cAttr.addChild( aKeepMatrix );
	cAttr.addChild( aAnimCurve );
	cAttr.addChild( aAnimCurveOutput );
	cAttr.setArray( true );

	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBlendMeshInfos ) );

	aUpdateMeshData = nAttr.create( "updateMeshData", "updateMeshData", MFnNumericData::kBoolean, false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpdateMeshData ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aDriverWeights,  outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMinusWeightEnable,  outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBlendMeshInfos, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpdateMeshData, outputGeom ) );

	return MS::kSuccess;
}


MStatus blendAndFixedShape::setDependentsDirty( const MPlug& dirtyPlug, MPlugArray& affectedPlugs )
{
	MStatus status;
	
	if( dirtyPlug.attribute() == aInputMesh )
	{
		MPlug parentPlug = dirtyPlug.parent();
		int infoIndex = parentPlug.logicalIndex();

		updateBlendMeshIndices.append( infoIndex );
	}

	if( dirtyPlug.attribute() == aDeltas )
	{
		MPlug parentPlug = dirtyPlug.parent();
		int infoIndex = parentPlug.logicalIndex();

		updateDeltaIndices.append( infoIndex );
	}
	return MS::kSuccess;
}