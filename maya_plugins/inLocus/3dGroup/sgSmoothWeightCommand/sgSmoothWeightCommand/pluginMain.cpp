
#include "sgSmoothWeightCommand.h"

#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerCommand( "sgSmoothWeightCommand", sgSmoothWeightCommand::creator,
		sgSmoothWeightCommand::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterCommand( "sgSmoothWeightCommand" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}
