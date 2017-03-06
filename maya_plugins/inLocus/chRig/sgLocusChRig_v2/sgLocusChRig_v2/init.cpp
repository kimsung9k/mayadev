#include "angleDriver.h"
#include "smartOrient.h"
#include "ikStretch.h"
#include "twoSideSlidingDistance.h"
#include "multMatrixDecompose.h"
#include "blendTwoMatrixDecompose.h"
#include "verticalVector.h"
#include "splineCurveInfo.h"
#include "distanceSeparator.h"
#include "controlerShape.h"
#include "footControl.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "smartOrient", smartOrient::id, smartOrient::creator,
								  smartOrient::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}
	status = plugin.registerNode( "ikStretch", ikStretch::id, ikStretch::creator,
								  ikStretch::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}
	status = plugin.registerNode( "twoSideSlidingDistance", twoSideSlidingDistance::id, twoSideSlidingDistance::creator,
								  twoSideSlidingDistance::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "multMatrixDecompose", multMatrixDecompose::id, multMatrixDecompose::creator,
								  multMatrixDecompose::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "blendTwoMatrixDecompose", blendTwoMatrixDecompose::id, blendTwoMatrixDecompose::creator,
								  blendTwoMatrixDecompose::initialize );
	if (!status) {
		status.perror("registerNode blendTwoMatrixDecompose");
		return status;
	}

	status = plugin.registerNode( "verticalVector", verticalVector::id, verticalVector::creator,
								  verticalVector::initialize );
	if (!status) {
		status.perror("registerNode verticalVector");
		return status;
	}

	status = plugin.registerNode( "splineCurveInfo", splineCurveInfo::id, splineCurveInfo::creator,
								  splineCurveInfo::initialize );
	if (!status) {
		status.perror("registerNode splineCurveInfo");
		return status;
	}

	status = plugin.registerNode( "distanceSeparator", distanceSeparator::id, distanceSeparator::creator,
								  distanceSeparator::initialize );
	if (!status) {
		status.perror("registerNode distanceSeparator");
		return status;
	}

	status = plugin.registerNode( "controlerShape", controlerShape::id, controlerShape::creator,
								  controlerShape::initialize );
	if (!status) {
		status.perror("registerNode controlerShape");
		return status;
	}

	status = plugin.registerNode( "footControl", footControl::id, footControl::creator,
								  footControl::initialize );
	if (!status) {
		status.perror("registerNode footControl");
		return status;
	}

	status = plugin.registerNode( "angleDriver", angleDriver::id, angleDriver::creator,
								  angleDriver::initialize );
	if (!status) {
		status.perror("registerNode footControl");
		return status;
	}

	return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( smartOrient::id );
	
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( ikStretch::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( twoSideSlidingDistance::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( multMatrixDecompose::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( blendTwoMatrixDecompose::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	
	status = plugin.deregisterNode( verticalVector::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( splineCurveInfo::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( distanceSeparator::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( controlerShape::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	status = plugin.deregisterNode( footControl::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	status = plugin.deregisterNode( angleDriver::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	return MS::kSuccess;
}
