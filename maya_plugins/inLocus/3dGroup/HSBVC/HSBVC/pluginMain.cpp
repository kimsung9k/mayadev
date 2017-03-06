//
// Copyright (C) Locus
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//

#include "volumeCurvesOnSurface.h"
#include "clusterControledCurve.h"
#include "splineMatrix.h"
#include "clusterControledSurface.h"
#include "matrixFromPolygon.h"
#include "simulatedCurveControledSurface.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "volumeCurvesOnSurface", volumeCurvesOnSurface::id, volumeCurvesOnSurface::creator,
								  volumeCurvesOnSurface::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.registerNode( "clusterControledCurve", clusterControledCurve::id, clusterControledCurve::creator,
								  clusterControledCurve::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.registerNode( "clusterControledSurface", clusterControledSurface::id, clusterControledSurface::creator,
								  clusterControledSurface::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.registerNode( "splineMatrix", splineMatrix::id, splineMatrix::creator,
								  splineMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.registerNode( "matrixFromPolygon", matrixFromPolygon::id, matrixFromPolygon::creator,
								  matrixFromPolygon::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.registerNode( "simulatedCurveControledSurface", simulatedCurveControledSurface::id, simulatedCurveControledSurface::creator,
								  simulatedCurveControledSurface::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( volumeCurvesOnSurface::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( clusterControledCurve::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( clusterControledSurface::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( splineMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( matrixFromPolygon::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( simulatedCurveControledSurface::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );/**/

	return status;
}
