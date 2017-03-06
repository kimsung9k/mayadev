#include "meshSnapCommand.h"
#include "meshSnapDeformer.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "Chad Vernon", "1.0", "Any" );

    status = fnPlugin.registerCommand( "meshSnap",
        MeshSnapCommand::creator,
        MeshSnapCommand::newSyntax );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    status = fnPlugin.registerNode( "meshSnap",
        MeshSnap::id,
        MeshSnap::creator,
        MeshSnap::initialize,
        MPxNode::kDeformerNode );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );

    status = fnPlugin.deregisterCommand( "meshSnap" );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    status = fnPlugin.deregisterNode( MeshSnap::id );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}