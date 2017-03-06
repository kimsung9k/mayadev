#include "sgBLocator_fromGeo.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "sggim", "1.0", "Any" );

    status = fnPlugin.registerNode( "sgBLocator_fromGeo", sgBLocator_fromGeo::id, sgBLocator_fromGeo::creator,
								  sgBLocator_fromGeo::initialize, MPxNode::kLocatorNode );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );

    status = fnPlugin.deregisterNode( sgBLocator_fromGeo::id );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}