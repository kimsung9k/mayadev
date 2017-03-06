//
// Copyright (C) Locus
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//

#include "sgIkSmoothStretch.h"

#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "ikSmoothStretch", sgIkSmoothStretch::id, sgIkSmoothStretch::creator,
								  sgIkSmoothStretch::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( sgIkSmoothStretch::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	return MS::kSuccess;
}