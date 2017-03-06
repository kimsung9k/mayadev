#include "keepRoundDeformer.h"
#include "slidingDeformer.h"
#include "slidingDeformer2.h"
#include "getLowerestValue.h"
#include "aimObjectMatrix.h"
#include "meshRivet.h"
#include "CollisionJointNode.h"
#include "blendCurve.h"

#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "keepRoundDeformer", keepRoundDeformer::id, keepRoundDeformer::creator,
		keepRoundDeformer::initialize, keepRoundDeformer::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "slidingDeformer_before", slidingDeformer::id, slidingDeformer::creator,
		slidingDeformer::initialize, slidingDeformer::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "slidingDeformer", slidingDeformer2::id, slidingDeformer2::creator,
		slidingDeformer2::initialize, slidingDeformer2::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "blendCurve", blendCurve::id, blendCurve::creator,
		blendCurve::initialize, blendCurve::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "getLowerestValue", getLowerestValue::id, getLowerestValue::creator,
		getLowerestValue::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.registerNode( "aimObjectMatrix", aimObjectMatrix::id, aimObjectMatrix::creator,
		aimObjectMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "meshRivet", meshRivet::id, meshRivet::creator,
		meshRivet::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "collisionJoint", CollisionJoint::id, CollisionJoint::creator,
		CollisionJoint::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	/*
	status = plugin.registerNode( "meshVtxAttachPoint", MeshVtxAttachPointNode::id, MeshVtxAttachPointNode::creator,
		MeshVtxAttachPointNode::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	*/
	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( keepRoundDeformer::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( slidingDeformer::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( slidingDeformer2::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( blendCurve::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( getLowerestValue::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.deregisterNode( aimObjectMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( meshRivet::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( CollisionJoint::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	/*
	status = plugin.deregisterNode( MeshVtxAttachPointNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	*/
	return status;
}