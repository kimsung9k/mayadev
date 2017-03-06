
#include <maya/MFnPlugin.h>
#include "sgSkinCluster.h"


MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "skkim", "1.0", "Any" );

	status = fnPlugin.registerNode( "sgSkinCluster", sgSkinCluster::id, sgSkinCluster::creator,
		sgSkinCluster::initialize, MPxNode::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );
	fnPlugin.deregisterNode( sgSkinCluster::id );

    return MS::kSuccess;
}