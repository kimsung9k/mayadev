#include "shoulderOrient.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "characterRigCustom", "2013", "Any");

	status = plugin.registerNode( "shoulderOrient", shoulderOrient::id, shoulderOrient::creator,
								  shoulderOrient::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( shoulderOrient::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	return status;
}