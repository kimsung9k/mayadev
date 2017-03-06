#include "CollisionJointNode.h"


MStatus CollisionJoint::clearMatrix( MDataBlock& data )
{
	MStatus status;
	if( !m_dirtyMatrix ) return MS::kSuccess;
	MArrayDataHandle hArrInputMatrix = data.inputArrayValue( aInputMatrix );
	m_mtxArrWorld.setLength( hArrInputMatrix.elementCount() );

	for( int i=0; i<hArrInputMatrix.elementCount(); i++, hArrInputMatrix.next() )
	{
		m_mtxArrWorld[i] = hArrInputMatrix.inputValue().asMatrix();
	}
	return MS::kSuccess;
}


MStatus CollisionJoint::clearMeshMatrix( MDataBlock& data )
{
	MStatus status;
	if( !m_dirtyMatrix && !m_dirtyMeshMatrix ) return MS::kSuccess;
	m_mtxMesh = data.inputValue( aMeshMatrix ).asMatrix();
	MMatrix m_mtxInvMesh = m_mtxMesh.inverse();

	for( int i=0; i<m_mtxArrWorld.length(); i++ )
	{
		m_mtxArrLocal[i] = m_mtxArrWorld[i]*m_mtxInvMesh;
	}
	return MS::kSuccess;
}


MStatus CollisionJoint::clearMesh( MDataBlock& data )
{
	MStatus status;
	if( !m_dirtyMesh ) return MS::kSuccess;
	MDataHandle hMesh = data.inputValue( aMesh, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = m_mesh.setObject( hMesh.asMesh() );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	return MS::kSuccess;
}


MStatus CollisionJoint::clearAxis( MDataBlock& data )
{
	MStatus status;
	if( !m_dirtyAxis ) return MS::kSuccess;
	m_aimIndex = data.inputValue( aAimAxis ).asUChar();
	m_upIndex  = data.inputValue( aUpAxis ).asUChar();

	return MS::kSuccess;
}


MStatus CollisionJoint::clearLockRate( MDataBlock& data )
{
	MStatus status;
	if( !m_dirtyAngleLockRate ) return MS::kSuccess;
	m_angleRate = data.inputValue( aAngleLockRate ).asFloat();
	return MS::kSuccess;
}


MStatus CollisionJoint::defaultOutputCaculate()
{
	if( !m_dirtyMatrix && !m_dirtyMesh && !m_dirtyMeshMatrix ) return MS::kSuccess;
	if( m_angleRate == 1.0f ) return MS::kSuccess;


}