#include "sgSlidingDeformer.h"


MTypeId     sgSlidingDeformer::id( 0x2015052700 );

MObject     sgSlidingDeformer::aSlidingBaseMesh;
MObject     sgSlidingDeformer::aMoveMesh;


sgSlidingDeformer::sgSlidingDeformer()
{
	m_pMeshIntersector = new MMeshIntersector;
	m_isSlidingBaseDirty = true;
	m_isMoveMeshDirty = true;
	m_isOrigMeshDirty = true;
	m_numThread = 48;

	m_pTask   = new sgSlidingDeformerTask;
	m_pThread = new sgSlidingDeformerThread[ m_numThread ];
	MThreadPool::init();
}


sgSlidingDeformer::~sgSlidingDeformer()
{
	delete m_pMeshIntersector;

	delete m_pTask;
	delete []m_pThread;
	MThreadPool::release();
}


MStatus sgSlidingDeformer::deform( MDataBlock& data, MItGeometry& iter, 
	const MMatrix& mat, unsigned int index )
{
	MStatus status;

	float env = data.inputValue( envelope ).asFloat();
	if( env == 0 ) return MS::kSuccess;

	m_pTask->env = env;

	float  timeValue;
	bool   timeError;

	if( m_isSlidingBaseDirty )
	{
		//cout << "sliding base is dirty" << endl;
		MObject oMesh = data.inputValue( aSlidingBaseMesh ).asMesh();
		m_meshSlidingBase.setObject( oMesh );
		m_pMeshIntersector->create( oMesh );
	}

	//check_time_start();

	if( m_isOrigMeshDirty )
	{
		//cout << "origMesh is dirty" << endl;
		iter.allPositions( m_pointsBase );
	}

	if( m_isMoveMeshDirty )
	{
		//cout << "moveMesh is dirty" << endl;
		MObject oMesh = data.inputValue( aMoveMesh ).asMesh(); 
		m_meshMove.setObject( oMesh );
		m_meshMove.getPoints( m_pointsMoved );
	}

	//check_time_end( timeValue,timeError );

	//cout << "dirtyCheck sec : " << timeValue << endl;

	if( m_pointsMoved.length() != iter.count() ) return MS::kSuccess;

	check_time_start();
	checkDeformedVertices( m_pointsBase, m_pointsMoved, m_indicesMoved );
	check_time_end( timeValue,timeError );

	//cout << "checkIndex sec : " << timeValue << endl;
	
	setThread();
	//check_time_start();
	computeSliding();
	check_time_end( timeValue,timeError );
	//endThread();

	//cout << "sliding sec : " << timeValue << endl;

	//check_time_start();
	iter.setAllPositions( m_pointsMoved );
	//check_time_end( timeValue,timeError );

	//cout << "setPosition sec : " << timeValue << endl;
	//cout << endl;

	m_isMoveMeshDirty    = false;
	m_isSlidingBaseDirty = false;
	m_isOrigMeshDirty    = false;

	return MS::kSuccess;
}


void* sgSlidingDeformer::creator()
{
	return new sgSlidingDeformer();
}


MStatus sgSlidingDeformer::initialize()
{
	MFnTypedAttribute tAttr;

	aSlidingBaseMesh = tAttr.create( "slidingBaseMesh", "slidingBaseMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aSlidingBaseMesh ) );

	aMoveMesh = tAttr.create( "moveMesh", "moveMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMoveMesh ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aSlidingBaseMesh, outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMoveMesh, outputGeom ) );

	return MS::kSuccess;
}


MStatus sgSlidingDeformer::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	if( plug == aSlidingBaseMesh )
	{
		m_isSlidingBaseDirty = true;
	}
	else if( plug == inputGeom )
	{
		m_isOrigMeshDirty = true;
	}
	else if( plug == aMoveMesh )
	{
		m_isMoveMeshDirty = true;
	}
	return MS::kSuccess;
}