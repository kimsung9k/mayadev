#include "sgBlendTwoMatrix.h"
#include "sgFollowMatrix.h"
#include  "sgMatrixToThreeByThree.h"
#include  "sgMultMatrixDecompose.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013.5", "Any");

	status = plugin.registerNode( "sgBlendTwoMatrix", sgBlendTwoMatrix::id, sgBlendTwoMatrix::creator,
								  sgBlendTwoMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgFollowMatrix", sgFollowMatrix::id, sgFollowMatrix::creator,
								  sgFollowMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgMatrixToThreeByThree", sgMatrixToThreeByThree::id, sgMatrixToThreeByThree::creator,
								  sgMatrixToThreeByThree::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "sgMultMatrixDecompose", sgMultMatrixDecompose::id, sgMultMatrixDecompose::creator,
								  sgMultMatrixDecompose::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( sgBlendTwoMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgFollowMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgMatrixToThreeByThree::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgMultMatrixDecompose::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}
