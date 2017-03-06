#include "sgEpBindNode.h"
#include "sgEpCurveNode.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "epCurveNode", sgEpCurveNode::id, sgEpCurveNode::creator,
								  sgEpCurveNode::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "epBindNode", sgEpBindNode::id, sgEpBindNode::creator,
								  sgEpBindNode::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( sgEpCurveNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgEpBindNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}
