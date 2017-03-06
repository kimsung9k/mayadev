//
// Copyright (C) Locus
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//

#include "sgLockAngleMatrix.h"
#include "sgVerticeToCurve.h"
#include "sgMatrixFromVertices.h"
#include "sgCurveFromPoints.h"
#include "sgSlidingDeformer.h"
#include "sgDynPointInMesh.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2014", "Any");

	status = plugin.registerNode( "sgLockAngleMatrix", sgLockAngleMatrix::id, sgLockAngleMatrix::creator,
								  sgLockAngleMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.registerNode( "sgVerticeToCurve", sgVerticeToCurve::id, sgVerticeToCurve::creator,
								  sgVerticeToCurve::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgMatrixFromVertices", sgMatrixFromVertices::id, sgMatrixFromVertices::creator,
								  sgMatrixFromVertices::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgCurveFromPoints", sgCurveFromPoints::id, sgCurveFromPoints::creator,
								  sgCurveFromPoints::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgSlidingDeformer", sgSlidingDeformer::id, sgSlidingDeformer::creator,
		sgSlidingDeformer::initialize, MPxNode::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgDynPointInMesh", sgDynPointInMesh::id, sgDynPointInMesh::creator,
		sgDynPointInMesh::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( sgLockAngleMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgVerticeToCurve::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgMatrixFromVertices::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgCurveFromPoints::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgSlidingDeformer::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgDynPointInMesh::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}
