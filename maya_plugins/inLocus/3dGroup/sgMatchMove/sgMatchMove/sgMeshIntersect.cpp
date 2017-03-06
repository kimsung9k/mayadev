#include "sgMeshIntersect.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

MTypeId     sgMeshIntersect::id( 0x2014091700 );

MObject     sgMeshIntersect::aPointSource;
	MObject     sgMeshIntersect::aPointSourceX;
	MObject     sgMeshIntersect::aPointSourceY;
	MObject     sgMeshIntersect::aPointSourceZ;
MObject     sgMeshIntersect::aPointDest;
	MObject     sgMeshIntersect::aPointDestX;
	MObject     sgMeshIntersect::aPointDestY;
	MObject     sgMeshIntersect::aPointDestZ;
MObject     sgMeshIntersect::aInputMesh;
MObject     sgMeshIntersect::aInputMeshMatrix;
MObject     sgMeshIntersect::aParentInverseMatrix;
MObject     sgMeshIntersect::aOutPoint;
	MObject     sgMeshIntersect::aOutPointX;
	MObject     sgMeshIntersect::aOutPointY;
	MObject     sgMeshIntersect::aOutPointZ;

unsigned int sgMeshIntersect::m_nodeNumber;
MIntArray    sgMeshIntersect::m_existingNodeNumbers;
MIntArray    sgMeshIntersect::m_existingNodeNumbersMap;

sgMeshIntersect::sgMeshIntersect()
{
	m_isDirtyPointSrc = true;
	m_isDirtyPointDest = true;
	m_isDirtyMesh = true;
	m_isDirtyMeshMatrix = true;
	m_pointsIntersect.append( MPoint( 0,0,0 ) );
	/*
	m_thisNodeNumber = m_nodeNumber;
	m_existingNodeNumbers.append( m_thisNodeNumber );
	m_existingNodeNumbersMap.setLength( m_thisNodeNumber+1 );
	m_existingNodeNumbersMap[ m_thisNodeNumber ] = m_existingNodeNumbers.length()-1;
	m_nodeNumber++;
	*/
}

sgMeshIntersect::~sgMeshIntersect()
{
}

MStatus sgMeshIntersect::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	if( m_isDirtyMeshMatrix )
	{
		MDataHandle hInputMeshMatrix = data.inputValue( aInputMeshMatrix );
		m_mtxMesh    = hInputMeshMatrix.asMatrix();
		m_mtxInvMesh = m_mtxMesh.inverse();
	}

	if( m_isDirtyMesh )
	{
		MDataHandle hInputMesh = data.inputValue( aInputMesh );
		m_fnMesh.setObject( hInputMesh.asMesh() );
	}

	if( m_isDirtyPointDest )
	{
		MDataHandle hPointDest   = data.inputValue( aPointDest );
		m_pointDest   = MPoint( hPointDest.asVector() ) * m_mtxInvMesh;
	}

	if( m_isDirtyPointSrc )
	{
		MDataHandle hPointSource = data.inputValue( aPointSource );
		m_pointSource = MPoint( hPointSource.asVector() ) * m_mtxInvMesh;
	}

	m_rayDirection = m_pointDest - m_pointSource;

	m_fnMesh.intersect( m_pointSource, m_rayDirection, m_pointsIntersect, &status );
	if( !status ) return MS::kSuccess;

	MDataHandle hParentInverse = data.inputValue( aParentInverseMatrix );
	m_mtxParentInverse = hParentInverse.asMatrix();

	MDataHandle hOutPoint = data.outputValue( aOutPoint );
	hOutPoint.setMVector( m_pointsIntersect[0]*m_mtxMesh*m_mtxParentInverse );

	return MS::kSuccess;
}

void* sgMeshIntersect::creator()
{
	return new sgMeshIntersect();
}

MStatus sgMeshIntersect::initialize()	
{
	MStatus				status;
	MFnNumericAttribute nAttr;
	MFnTypedAttribute   tAttr;
	MFnMatrixAttribute  mAttr;

	aPointSourceX = nAttr.create( "pointSourceX", "psx", MFnNumericData::kDouble, 0.0 );
	aPointSourceY = nAttr.create( "pointSourceY", "psy", MFnNumericData::kDouble, 0.0 );
	aPointSourceZ = nAttr.create( "pointSourceZ", "psz", MFnNumericData::kDouble, 0.0 );
	aPointSource  = nAttr.create( "pointSource", "ps", aPointSourceX, aPointSourceY, aPointSourceZ );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPointSource ) );

	aPointDestX = nAttr.create( "pointDestX", "pdx", MFnNumericData::kDouble, 0.0 );
	aPointDestY = nAttr.create( "pointDestY", "pdy", MFnNumericData::kDouble, 0.0 );
	aPointDestZ = nAttr.create( "pointDestZ", "pdz", MFnNumericData::kDouble, 0.0 );
	aPointDest  = nAttr.create( "pointDest", "pd", aPointDestX, aPointDestY, aPointDestZ );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aPointDest ) );

	aInputMesh = tAttr.create( "inputMesh", "inMesh", MFnData::kMesh );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );

	aInputMeshMatrix = mAttr.create( "inputMeshMatrix", "inMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshMatrix ) );

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aParentInverseMatrix ) );

	aOutPointX = nAttr.create( "outPointX", "opx", MFnNumericData::kDouble, 0.0 );
	aOutPointY = nAttr.create( "outPointY", "opy", MFnNumericData::kDouble, 0.0 );
	aOutPointZ = nAttr.create( "outPointZ", "opz", MFnNumericData::kDouble, 0.0 );
	aOutPoint  = nAttr.create( "outPoint", "op", aOutPointX, aOutPointY, aOutPointZ );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutPoint ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPointSource, aOutPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aPointDest, aOutPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aParentInverseMatrix, aOutPoint ) );

	m_nodeNumber = 0;

	return MS::kSuccess;
}


MStatus  sgMeshIntersect::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus ststus;

	if( plug == aPointSource )
	{
		m_isDirtyPointSrc = true;
	}
	if( plug == aPointDest )
	{
		m_isDirtyPointDest = true;
	}
	if( plug == aInputMesh )
	{
		m_isDirtyMesh = true;
	}
	if( plug == aInputMeshMatrix )
	{
		m_isDirtyMeshMatrix = true;
	}

	return MS::kSuccess;
}