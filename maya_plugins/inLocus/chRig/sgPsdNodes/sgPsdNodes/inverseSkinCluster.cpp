#include "inverseSkinCluster.h"
#include "inverseSkinCluster_def.h"

MTypeId     inverseSkinCluster::id( 0xc8d601 );

MObject     inverseSkinCluster::aInMesh;
MObject     inverseSkinCluster::aGeomMatrix;

MObject     inverseSkinCluster::aMatrix;
MObject     inverseSkinCluster::aBindPreMatrix;
MObject     inverseSkinCluster::aUpdateMatrix;

MObject     inverseSkinCluster::aTargetSkinCluster;
MObject     inverseSkinCluster::aUpdateWeightList;


inverseSkinCluster::inverseSkinCluster() 
{
	weightListUpdated = false;
	matrixAttrUpdated = true;
	matrixInfoUpdated = false;
	originalMeshUpdated = true;
	pSkinInfo = new skinClusterInfo;
	pTaskData = new taskData0;
	logicalIndexArray.setLength( 0 );
	MThreadPool::init();
}

inverseSkinCluster::~inverseSkinCluster() 
{
	delete pSkinInfo;
	delete pTaskData;
	MThreadPool::release();
}


MStatus inverseSkinCluster::deform( MDataBlock& data,
									   MItGeometry& itGeo,
									   const MMatrix& localToWorldMatrix,
									   unsigned int geomIndex )
{
	MStatus status;

	MMatrix geomMatrix;
	bool updateSkinInfo;

	MDataHandle hInMesh = data.inputValue( aInMesh, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MObject oInMesh = hInMesh.asMesh();
	if( oInMesh.isNull() )
		return MS::kFailure;
	MFnMesh inMesh = oInMesh;
	inMesh.getPoints( m_meshPoints );

	if( originalMeshUpdated )
	{
		itGeo.allPositions( pTaskData->basePoints );
		originalMeshUpdated = false;
	}

	MDataHandle hGeomMatrix = data.inputValue( aGeomMatrix );
	geomMatrix = hGeomMatrix.asMatrix();

	MDataHandle hUpdateWeightList = data.inputValue( aUpdateWeightList );
	updateSkinInfo = hUpdateWeightList.asBool();

	MDataHandle hEnvelop = data.inputValue( envelope );
	envelopValue = hEnvelop.asFloat();

	pTaskData->envelop = envelopValue;
	pTaskData->invEnv  = 1.0f - envelopValue;
	pTaskData->beforePoints = m_meshPoints;

	if( updateSkinInfo )
	{	
		MDataHandle hUpdateSkinInfoOutput = data.outputValue( aUpdateWeightList );
		hUpdateSkinInfoOutput.set( false );
		weightListUpdated = false;
	}

	if( logicalIndexArray.length() == 0 )
		updateLogicalIndexArray();

	MDataHandle hUpdateMatrix = data.inputValue( aUpdateMatrix );

	if( hUpdateMatrix.asBool() )
	{
		matrixAttrUpdated = false;
		matrixInfoUpdated = false;
	}

	MArrayDataHandle hArrMatrix = data.inputArrayValue( aMatrix );
	MArrayDataHandle hArrBindPreMatrix = data.inputArrayValue( aBindPreMatrix );
	updateMatrixAttribute( hArrMatrix, hArrBindPreMatrix );

	if( !matrixInfoUpdated )
	{
		updateMatrixInfo( hArrMatrix, hArrBindPreMatrix );
	}

	if( !weightListUpdated )
	{
		pTaskData->afterPoints.setLength( m_meshPoints.length() );
		pTaskData->envPoints.setLength( m_meshPoints.length() );

		updateWeightList();
	}

	if( !matrixInfoUpdated || !weightListUpdated )
	{
		if( pSkinInfo->weightsArray.size() > 0 )
			getWeightedMatrices( geomMatrix );
		else
			return MS::kFailure;

		matrixInfoUpdated = true;
		weightListUpdated = true;
	}

	if( envelopValue )
	{
		setThread();
		MThreadPool::newParallelRegion( parallelCompute, pThread );
		endThread();

		itGeo.setAllPositions( pTaskData->envPoints );
	}
	else
	{
		itGeo.setAllPositions( pTaskData->basePoints );
	}

	return MS::kSuccess;
}


void* inverseSkinCluster::creator()
{
	return new inverseSkinCluster();
}


MStatus inverseSkinCluster::initialize()
{
	MStatus   status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnMessageAttribute msgAttr;
	MFnTypedAttribute tAttr;

	aInMesh = tAttr.create( "inMesh", "inMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInMesh ) );

	aGeomMatrix = mAttr.create( "geomMatrix", "geomMatrix" );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aGeomMatrix ) );

	aMatrix = mAttr.create( "matrix", "matrix" );
	mAttr.setArray( true );
	mAttr.setStorable( true );
	mAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMatrix ) );

	aBindPreMatrix = mAttr.create( "bindPreMatrix", "bindPreMatrix" );
	mAttr.setArray( true );
	mAttr.setStorable( true );
	mAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBindPreMatrix ) );

	aUpdateMatrix = nAttr.create( "updateMatrix", "updateMatrix", MFnNumericData::kBoolean, false );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpdateMatrix ) );

	aTargetSkinCluster = msgAttr.create( "targetSkinCluster", "targetSkinCluster" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTargetSkinCluster ) );

	aUpdateWeightList = nAttr.create( "updateWeightList", "updateWeightList", MFnNumericData::kBoolean, false );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpdateWeightList ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInMesh, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aGeomMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBindPreMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpdateMatrix, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpdateWeightList, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTargetSkinCluster, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMatrix, outputGeom ) );

	return MS::kSuccess;
}