#include "slidingDeformer2.h"


MTypeId     slidingDeformer2::id( 0x0ec1200 );

MObject     slidingDeformer2::aBaseMesh;
MObject     slidingDeformer2::aOrigMesh;
MObject     slidingDeformer2::aCheckAllPoints;
MObject     slidingDeformer2::aCheckTime;


slidingDeformer2::slidingDeformer2()
{
	m_pMeshIntersector = new MMeshIntersector;
	m_isBaseMeshDirty = true;
	m_isOrigMeshDirty = true;
	m_isInputGeomDirty = true;
	m_numThread = 48;

	m_pTaskChkIndices = new slidingDeformer2ChkIndicesTask;
	m_pThreadChkIndices = new slidingDeformer2ChkIndicesThread[ m_numThread ];
	m_pTaskGetDist = new slidingDeformer2GetDistTask;
	m_pThreadGetDist = new slidingDeformer2GetDistThread[ m_numThread ];
	m_pTaskSliding = new slidingDeformer2SlidingTask;
	m_pThreadSliding = new slidingDeformer2SlidingThread[ m_numThread ];
	MThreadPool::init();
}


slidingDeformer2::~slidingDeformer2()
{
	delete m_pMeshIntersector;

	delete m_pTaskSliding;
	delete []m_pThreadSliding;
	MThreadPool::release();
}


MStatus slidingDeformer2::deform( MDataBlock& data, MItGeometry& iter, 
	const MMatrix& mat, unsigned int index )
{
	MStatus status;
	m_env = data.inputValue( envelope ).asFloat();
	if( m_env  < 0.0001 ) return MS::kSuccess;

	float timeValue;
	bool   timeError;

	check_time_start();

	m_checkAllPoints = data.inputValue( aCheckAllPoints ).asBool();

	if( m_isBaseMeshDirty )
	{
		MObject oMesh = data.inputValue( aBaseMesh ).asMesh(); 
		if( oMesh.isNull() ) return MS::kSuccess;
		m_pMeshIntersector->create( oMesh );
		m_isBaseMeshDirty = false;
	}

	if( m_isOrigMeshDirty )
	{
		MObject oMesh = data.inputValue( aOrigMesh ).asMesh();
		MFnMesh meshOrig = oMesh;
		if( oMesh.isNull() ) return MS::kSuccess;
		meshOrig.getPoints( m_pointsOrig );
		m_vectorArr.setLength( m_pointsOrig.length() );

		getSlidingDistance();

		m_indicesAllPoints.setLength( m_pointsOrig.length() );
		for( unsigned int i=0; i< m_indicesAllPoints.length(); i++ )
		{
			m_indicesAllPoints[i]=i;
		}

		m_isOrigMeshDirty = false;
	}

	if( m_isInputGeomDirty )
	{
		iter.allPositions( m_pointsMoved );
		m_pointsResult = m_pointsMoved;
		m_isInputGeomDirty = false;
	}

	if( m_pointsMoved.length() != m_pointsOrig.length() ) return MS::kSuccess;
	
	checkDeformedVertices();
	sliding();
	check_time_end( timeValue,timeError );
	iter.setAllPositions( m_pointsResult );

	if( data.inputValue( aCheckTime ).asBool() )
	{
		cout << "check all deform : " << m_checkAllPoints << endl;
		cout << "Caculate Time : " << timeValue << endl;
	}

	return MS::kSuccess;
}

void* slidingDeformer2::creator()
{
	return new slidingDeformer2();
}

MStatus slidingDeformer2::initialize()
{
	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;

	aBaseMesh = tAttr.create( "baseMesh", "baseMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMesh ) );

	aOrigMesh = tAttr.create( "origMesh", "origMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOrigMesh ) );

	aCheckAllPoints = nAttr.create( "checkAllPoints", "checkAllPoints", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCheckAllPoints ) );

	aCheckTime = nAttr.create( "checkTime", "checkTime", MFnNumericData::kBoolean, false );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCheckTime ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMesh, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aOrigMesh, outputGeom ) );

	return MS::kSuccess;
}

MStatus slidingDeformer2::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	if( plug == aBaseMesh )
	{
		m_isBaseMeshDirty = true;
	}
	else if( plug == aOrigMesh )
	{
		m_isOrigMeshDirty = true;
	}
	else if( plug == inputGeom )
	{
		m_isInputGeomDirty = true;
	}
	return MS::kSuccess;
}