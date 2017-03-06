//
// Copyright (C) locus
// 
// File: CollisionJointNode.cpp
//
// Dependency Graph Node: CollisionJoint
//
// Author: Maya Plug-in Wizard 2.0
//

#include "CollisionJointNode.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

MTypeId     CollisionJoint::id( 0x00001 );

// Example attributes
// 
MObject     CollisionJoint::aInputMatrix;
MObject     CollisionJoint::aMesh;
MObject     CollisionJoint::aMeshMatrix;
MObject     CollisionJoint::aAimAxis;
MObject     CollisionJoint::aUpAxis;
MObject     CollisionJoint::aAngleLockRate;
MObject     CollisionJoint::aOutputMatrix;       

CollisionJoint::CollisionJoint()
{
	m_dirtyMatrix = true;
	m_dirtyMesh = true;
	m_dirtyMeshMatrix = true;
	m_dirtyAxis = true;
	m_dirtyAngleLockRate = true;
}

CollisionJoint::~CollisionJoint() {}

MStatus CollisionJoint::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;

	clearMatrix( data );
	clearMeshMatrix( data );
	clearMesh( data );
	clearAxis( data );
	clearLockRate( data );

	m_dirtyMatrix = false;
	m_dirtyMesh   = false;
	m_dirtyMeshMatrix = false;
	m_dirtyAxis = false;
	m_dirtyAngleLockRate = false;

	return MS::kSuccess;
}

void* CollisionJoint::creator()
{
	return new CollisionJoint();
}

MStatus CollisionJoint::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute  mAttr;
	MFnTypedAttribute   tAttr;
	MFnEnumAttribute    eAttr;

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	mAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMatrix ) );

	aMesh = tAttr.create( "mesh", "mesh", MFnData::kMesh );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMesh ) );

	aMeshMatrix = mAttr.create( "meshMatrix", "meshMatrix" );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMeshMatrix ) );

	aAimAxis = eAttr.create( "aimAxis", "aimAxis" );
	eAttr.addField( "X", 0 ), eAttr.addField( "Y", 1 ), eAttr.addField( "Z", 2 );
	eAttr.addField( "-X", 3 ), eAttr.addField( "-Y", 4 ), eAttr.addField( "-Z", 5 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAimAxis ) );

	aUpAxis = eAttr.create( "upAxis", "upAxis" );
	eAttr.addField( "X", 0 ), eAttr.addField( "Y", 1 ), eAttr.addField( "Z", 2 );
	eAttr.addField( "-X", 3 ), eAttr.addField( "-Y", 4 ), eAttr.addField( "-Z", 5 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aUpAxis ) );

	aAngleLockRate = nAttr.create( "angleLockRate", "angleLockRate", MFnNumericData::kFloat, 0.0 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAngleLockRate ) );

	aOutputMatrix = mAttr.create( "outputMatrix", "outputMatrix" );
	mAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT ( addAttribute( aOutputMatrix ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMatrix, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aMesh, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAimAxis, aOutputMatrix ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aUpAxis, aOutputMatrix ) );

	return MS::kSuccess;
}


MStatus CollisionJoint::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMatrix )
	{
		m_dirtyMatrix = true;
	}
	else if( plug == aMeshMatrix )
	{
		m_dirtyMeshMatrix = true;
	}
	else if( plug == aMesh )
	{
		m_dirtyMesh = true;
	}
	else if( plug == aAimAxis || plug == aUpAxis )
	{
		m_dirtyAxis = true;
	}
	else if( plug == aAngleLockRate )
	{
		m_dirtyAngleLockRate = true;
	}

	return status;
}