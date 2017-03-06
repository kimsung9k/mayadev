#include "keepRoundDeformer.h"

MTypeId     keepRoundDeformer::id( 0x0ec0700 );

MObject     keepRoundDeformer::aBaseMesh;     
MObject     keepRoundDeformer::aInputMatrix; 

keepRoundDeformer::keepRoundDeformer()
{
	m_isOrigGeomDirty = true;
	m_isBaseGeomDirty = true;
	m_isMatrixDirty = true;
}
keepRoundDeformer::~keepRoundDeformer(){}


MStatus keepRoundDeformer::deform( MDataBlock& data, MItGeometry& iter, 
	const MMatrix& mat, unsigned int index )
{
	MStatus status;

	if( m_isOrigGeomDirty ){
		iter.allPositions( m_pointsOrig );

		m_outputPoints.setLength( m_pointsOrig.length() );
		m_isOrigGeomDirty = false;
		m_isMatrixDirty = true;
	}

	if( m_isMatrixDirty )
	{
		MDataHandle hInputMatrix  = data.inputValue( aInputMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_matrix = hInputMatrix.asMatrix() * mat.inverse();
		m_isMatrixDirty = false;
		m_isBaseGeomDirty = true;
	}

	if( m_isBaseGeomDirty ){

		MDataHandle hEditGeom = data.inputValue( aBaseMesh, &status );
		MFnMesh fnEditMesh( hEditGeom.asMesh() );

		MPointArray points;
		fnEditMesh.getPoints( points );
		m_distsPoint.setLength( points.length() );

		MMatrix invMatrix = m_matrix.inverse();

		for( int i=0; i< m_distsPoint.length(); i++ )
		{
			m_distsPoint[i] = MVector( points[i]*invMatrix ).length();
		}
		m_isBaseGeomDirty = false;
	}

	if( m_pointsOrig.length() != m_distsPoint.length() )
	{
		return MS::kSuccess;
	}

	MDataHandle hEnvelope = data.inputValue( envelope );
	float envValue = hEnvelope.asFloat();

	if( envValue <= 0 ) return MS::kSuccess;

	editPointsWidthMatrix( m_distsPoint, m_pointsOrig,
		                   m_outputPoints, m_matrix, envValue );

	iter.setAllPositions( m_outputPoints );

	return MS::kSuccess;
}

void* keepRoundDeformer::creator()
{
	return new keepRoundDeformer();
}

MStatus keepRoundDeformer::initialize()
{
	MStatus status;
	MFnMatrixAttribute  mAttr;
	MFnTypedAttribute   tAttr;

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMatrix, outputGeom ) );

	aBaseMesh = tAttr.create( "baseMesh", "baseMesh", MFnData::kMesh );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseMesh ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBaseMesh, outputGeom ) );

	return MS::kSuccess;
}

MStatus keepRoundDeformer::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	if( plug == aInputMatrix )
	{
		m_isMatrixDirty = true;
	}
	else if( plug == inputGeom )
	{
		m_isOrigGeomDirty = true;
	}
	else if( plug == aBaseMesh )
	{
		m_isBaseGeomDirty = true;
	}
	return MS::kSuccess;
}