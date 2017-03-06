#include "sgMeshIntersect.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2014", "Any");

	status = plugin.registerNode( "sgMeshIntersect", sgMeshIntersect::id, sgMeshIntersect::creator,
								  sgMeshIntersect::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( sgMeshIntersect::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}
