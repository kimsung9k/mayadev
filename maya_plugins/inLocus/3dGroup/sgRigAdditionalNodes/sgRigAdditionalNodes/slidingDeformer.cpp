#include "slidingDeformer.h"


MTypeId     slidingDeformer::id( 0x0ec0900 );

MObject     slidingDeformer::aBaseMesh;

slidingDeformer::slidingDeformer()
{
	m_pMeshIntersector = new MMeshIntersector;
	m_isBaseMeshDirty = true;
	m_isOrigMeshDirty = true;
	m_numThread = 48;

	m_pTask = new slidingDeformerTask;
	m_pThread = new slidingDeformerThread[ m_numThread ];
	MThreadPool::init();
}
slidingDeformer::~slidingDeformer()
{
	delete m_pMeshIntersector;

	delete m_pTask;
	delete []m_pThread;
	MThreadPool::release();
}


MStatus slidingDeformer::deform( MDataBlock& data, MItGeometry& iter, 
	const MMatrix& mat, unsigned int index )
{
	MStatus status;

	if( m_isBaseMeshDirty )
	{
		MObject oMesh = data.inputValue( aBaseMesh ).asMesh(); 
		m_meshBase.setObject( oMesh );
		m_meshBase.getPoints( m_pointsBase );
		m_pMeshIntersector->create( oMesh );
		m_isBaseMeshDirty = false;
	}

	if( m_isOrigMeshDirty )
	{
		iter.allPositions( m_pointsMoved );
		m_isOrigMeshDirty = false;
	}

	if( m_pointsMoved.length() != m_pointsBase.length() ) return MS::kSuccess;

	float timeValue;
	bool   timeError;

	check_time_start();
	checkDeformedVertices( m_pointsBase, m_pointsMoved, m_indicesMoved );
	check_time_end( timeValue,timeError );

	cout << "checkIndex sec : " << timeValue << endl;
	
	setThread();
	check_time_start();
	computeSliding();
	check_time_end( timeValue,timeError );
	endThread();

	cout << "sliding sec : " << timeValue << endl;

	check_time_start();
	iter.setAllPositions( m_pointsMoved );
	check_time_end( timeValue,timeError );

	cout << "setPosition sec : " << timeValue << endl;
	cout << endl;

	return MS::kSuccess;
}

void* slidingDeformer::creator()
{
	return new slidingDeformer();
}

MStatus slidingDeformer::initialize()
{
	MFnTypedAttribute tAttr;

	aBaseMesh = tAttr.create( "baseMesh", "baseMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMesh ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMesh, outputGeom ) );

	return MS::kSuccess;
}

MStatus slidingDeformer::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	if( plug == aBaseMesh )
	{
		m_isBaseMeshDirty = true;
	}
	else if( plug == inputGeom )
	{
		m_isOrigMeshDirty = true;
	}
	return MS::kSuccess;
}