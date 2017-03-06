#include "meshRivet.h"


MStatus meshRivet::setResult( const MPlug& plug, MDataBlock& data )
{
	if( !m_dirty )
	{
		if( plug == aOutMatrix )
		{
			MDataHandle hOutMatrix = data.outputValue( aOutMatrix );
			hOutMatrix.set( m_mtxResult );
		}
		else if( plug == aOutTranslate )
		{
			MDataHandle hOutTranslate = data.outputValue( aOutTranslate );
			hOutTranslate.setMVector( m_outputCenter );
		}
		else if( plug == aOutRotate )
		{
			MDataHandle hOutRotate = data.outputValue( aOutRotate );
			MTransformationMatrix trMtx( m_mtxResult );
			hOutRotate.set( trMtx.eulerRotation().asVector() );
		}
		return MS::kSuccess;
	}

	if( m_indicesCenterDirty || m_indicesAimDirty || m_indicesUpDirty || m_meshDirty )
	{
		unsigned int lenCenter = m_indicesCenter.length();
		unsigned int lenAim    = m_indicesAim.length();
		unsigned int lenUp     = m_indicesUp.length();

		unsigned int lenAimPiv = m_indicesAimPiv.length();
		unsigned int lenUpPiv  = m_indicesUpPiv.length();

		if( !lenCenter ) return MS::kFailure;
		if( !lenAim )return MS::kFailure;
		if( !lenUp )return MS::kFailure;

		MBoundingBox bb_center, bb_aimPiv, bb_aim, bb_upPiv, bb_up;
		if( !m_pointArr.length() ) return MS::kFailure;

		for( int i=0; i< lenCenter; i++ )
		{
			bb_center.expand( m_pointArr[ m_indicesCenter[i] ] );
		}
		for( int i=0; i< lenAim; i++ )
		{
			bb_aim.expand( m_pointArr[ m_indicesAim[i] ] );
		}
		for( int i=0; i< lenAimPiv; i++ )
		{
			bb_aimPiv.expand( m_pointArr[ m_indicesAimPiv[i] ] );
		}
		for( int i=0; i< lenUp; i++ )
		{
			bb_up.expand( m_pointArr[ m_indicesUp[i] ] );
		}
		for( int i=0; i< lenUpPiv; i++ )
		{
			bb_upPiv.expand( m_pointArr[ m_indicesUpPiv[i] ] );
		}
		m_localCenter = bb_center.center();

		if( lenAimPiv )
			m_localAim = bb_aim.center() - bb_aimPiv.center();
		else
			m_localAim = bb_aim.center() - m_localCenter;

		if( lenUpPiv )
			m_localUp = bb_up.center() - bb_upPiv.center();
		else
			m_localUp = bb_up.center() - m_localCenter;

		m_outputCenter = m_localCenter*m_mtxMult;
		m_outputAim    = m_localAim*m_mtxMult;
		m_outputUp     = m_localUp*m_mtxMult;

		m_indicesCenterDirty = false;
		m_indicesAimDirty = false;
		m_indicesUpDirty = false;
		m_meshDirty = false;
	}

	if( m_matrixDirty || m_parentInverseDirty )
	{
		m_outputCenter = m_localCenter*m_mtxMult;
		m_outputAim    = m_localAim*m_mtxMult;
		m_outputUp     = m_localUp*m_mtxMult;
		m_matrixDirty = false;
		m_parentInverseDirty = false;
	}

	int aimAxis = m_aimAxis;
	int upAxis  = m_upAxis;
	int crossAxis = 3 - aimAxis%3 - upAxis%3;

	bool inverseAim = false;
	bool inverseUp  = false;
	bool inverseCross = false;

	if( aimAxis > 2 )
	{
		aimAxis -= 3;
		inverseAim = true;
	}
	if( upAxis > 2 )
	{
		upAxis -= 3;
		inverseUp = true;
	}
	if( data.inputValue( aInverseCross ).asBool() )
	{
		inverseCross = true;
	}

	MVector resultAim, resultUp, resultCross;
	if( !inverseAim ) resultAim = m_outputAim;
	else resultAim = m_outputAim * -1.0;
	if( !inverseUp ) resultUp = m_outputUp;
	else resultUp  = m_outputUp * -1.0;
	if( !inverseCross ) resultCross = resultAim^resultUp;
	else resultCross = resultUp^resultAim;

	m_mtxResult( aimAxis, 0 ) = resultAim.x;
	m_mtxResult( aimAxis, 1 ) = resultAim.y;
	m_mtxResult( aimAxis, 2 ) = resultAim.z;
	m_mtxResult( upAxis, 0 ) = resultUp.x;
	m_mtxResult( upAxis, 1 ) = resultUp.y;
	m_mtxResult( upAxis, 2 ) = resultUp.z;
	m_mtxResult( crossAxis, 0 ) = resultCross.x;
	m_mtxResult( crossAxis, 1 ) = resultCross.y;
	m_mtxResult( crossAxis, 2 ) = resultCross.z;
	m_mtxResult( 3, 0 ) = m_outputCenter.x;
	m_mtxResult( 3, 1 ) = m_outputCenter.y;
	m_mtxResult( 3, 2 ) = m_outputCenter.z;

	if( plug == aOutMatrix )
	{
		MDataHandle hOutMatrix = data.outputValue( aOutMatrix );
		hOutMatrix.set( m_mtxResult );
	}
	else if( plug == aOutTranslate )
	{
		MDataHandle hOutTranslate = data.outputValue( aOutTranslate );
		hOutTranslate.setMVector( m_outputCenter );
	}
	else if( plug == aOutRotate )
	{
		MDataHandle hOutRotate = data.outputValue( aOutRotate );
		MTransformationMatrix trMtx( m_mtxResult );
		hOutRotate.set( trMtx.eulerRotation().asVector() );
	}
	
	m_dirty = false;

	return MS::kSuccess;
}


void  meshRivet::getMeshInfomation( MDataBlock& data )
{
	MFnMesh fnMesh( data.inputValue( aInputMesh ).asMesh() );
	fnMesh.getPoints( m_pointArr );
}


void  meshRivet::getMeshMatrix( MDataBlock& data )
{
	m_mtxMesh = data.inputValue( aMeshMatrix ).asMatrix();
	m_mtxMult = m_mtxMesh * m_mtxParentInverse;
}


void meshRivet::getParentInverseMatrix( MDataBlock& data )
{
	m_mtxParentInverse = data.inputValue( aParentInverseMatrix ).asMatrix();
	m_mtxMult = m_mtxMesh * m_mtxParentInverse;
}

void  meshRivet::getCenterIndices( MDataBlock& data )
{
	MArrayDataHandle hArrCenterIndices = data.inputArrayValue( aCenterIndices );
	
	m_indicesCenter.setLength( hArrCenterIndices.elementCount() );
	for( int i=0; i< hArrCenterIndices.elementCount(); i++, hArrCenterIndices.next() )
	{
		m_indicesCenter[i] = hArrCenterIndices.inputValue().asInt();
	}
}


void  meshRivet::getAimIndices( MDataBlock& data )
{
	MArrayDataHandle hArrAimIndices    = data.inputArrayValue( aAimIndices );

	m_indicesAim.setLength( hArrAimIndices.elementCount() );
	for( int i=0; i<hArrAimIndices.elementCount(); i++, hArrAimIndices.next() )
	{
		m_indicesAim[i] = hArrAimIndices.inputValue().asInt();
	}

	MArrayDataHandle hArrAimPivIndices    = data.inputArrayValue( aAimPivIndices );

	m_indicesAimPiv.setLength( hArrAimPivIndices.elementCount() );
	for( int i=0; i<hArrAimPivIndices.elementCount(); i++, hArrAimPivIndices.next() )
	{
		m_indicesAimPiv[i] = hArrAimPivIndices.inputValue().asInt();
	}
}


void  meshRivet::getUpIndices( MDataBlock& data )
{
	MArrayDataHandle hArrUpIndices     = data.inputArrayValue( aUpIndices );

	m_indicesUp.setLength( hArrUpIndices.elementCount() );
	for( int i=0; i<hArrUpIndices.elementCount(); i++, hArrUpIndices.next() )
	{
		m_indicesUp[i] = hArrUpIndices.inputValue().asInt();
	}

	MArrayDataHandle hArrUpPivIndices  = data.inputArrayValue( aUpPivIndices );

	m_indicesUpPiv.setLength( hArrUpPivIndices.elementCount() );
	for( int i=0; i<hArrUpPivIndices.elementCount(); i++, hArrUpPivIndices.next() )
	{
		m_indicesUpPiv[i] = hArrUpPivIndices.inputValue().asInt();
	}
}