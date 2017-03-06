#include "sgBDataCmd_Mesh.h"
#include "sgBDataCmd_key.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj, "sggim", "1.0", "Any" );
	status = fnPlugin.registerCommand( "sgBDataCmd_mesh", sgBDataCmd_mesh::creator, sgBDataCmd_mesh::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.registerCommand( "sgBDataCmd_key", sgBDataCmd_key::creator, sgBDataCmd_key::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin fnPlugin( obj );
	status = fnPlugin.deregisterCommand( "sgBDataCmd_mesh" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = fnPlugin.deregisterCommand( "sgBDataCmd_key" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}