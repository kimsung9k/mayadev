#include "wristAngle.h"
#include "shoulderOrient.h"
#include "squash.h"
#include "blendTwoMatrix.h"
#include "blendTwoAngle.h"
#include "matrixToThreeByThree.h"
#include "matrixToFourByFour.h"
#include "followMatrix.h"
#include "followDouble.h"

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>


MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2012", "Any");


	status = plugin.registerNode( "wristAngle", wristAngle::id, wristAngle::creator,
								  wristAngle::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "shoulderOrient", shoulderOrient::id, shoulderOrient::creator,
								  shoulderOrient::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "squash", squash::id, squash::creator,
								  squash::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "blendTwoMatrix", blendTwoMatrix::id, blendTwoMatrix::creator,
								  blendTwoMatrix::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "blendTwoAngle", blendTwoAngle::id, blendTwoAngle::creator,
								  blendTwoAngle::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "matrixToThreeByThree", matrixToThreeByThree::id, matrixToThreeByThree::creator,
								  matrixToThreeByThree::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "matrixToFourByFour", matrixToFourByFour::id, matrixToFourByFour::creator,
								  matrixToFourByFour::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "followMatrix", followMatrix::id, followMatrix::creator,
								  followMatrix::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = plugin.registerNode( "followDouble", followDouble::id, followDouble::creator,
								  followDouble::initialize );
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

	status = plugin.deregisterNode( wristAngle::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	status = plugin.deregisterNode( shoulderOrient::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	status = plugin.deregisterNode( squash::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( blendTwoMatrix::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( blendTwoAngle::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( matrixToThreeByThree::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( matrixToFourByFour::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( followMatrix::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	status = plugin.deregisterNode( followDouble::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	return status;
}