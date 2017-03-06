#include "sgPolyUnit.h"
#include "sgSeparate.h"
#include "sgGetMeshElementInfo.h"
#include "sgMeshSnap.h"

#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{
	MStatus status;

	MFnPlugin fnPlugin( obj, "Sg Gim", "1.0", "Any" );
	status = fnPlugin.registerNode( "sgPolyUnit",  sgPolyUnit::id, 
		sgPolyUnit::creator, sgPolyUnit::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.registerNode( "sgSeparate",  sgSeparate::id, 
		sgSeparate::creator, sgSeparate::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.registerNode( "sgMeshSnap",  sgMeshSnap::id,
		sgMeshSnap::creator, sgMeshSnap::initialize, MPxNode::kDeformerNode );

	status = fnPlugin.registerCommand( "sgGetMeshElementInfo", sgGetMeshElementInfo::creator,
		sgGetMeshElementInfo::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}



MStatus uninitializePlugin( MObject obj )
{
	MStatus status;

	MFnPlugin fnPlugin( obj );

	status = fnPlugin.deregisterNode( sgPolyUnit::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.deregisterNode( sgSeparate::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.deregisterNode( sgMeshSnap::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.deregisterCommand( "sgGetMeshElementInfo" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}