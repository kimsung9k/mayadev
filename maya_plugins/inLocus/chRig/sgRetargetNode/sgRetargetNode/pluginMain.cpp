#include "dgTransform.h"
#include "retargetBlender.h"
#include "udAttrBlender.h"
#include "retargetOrientNode.h"
#include "retargetTransNode.h"
#include "transRotateCombineMatrix.h"
#include "retargetLocator.h"
#include "meshShapeLocator.h"
#include "editMatrixByCurve.h"
#include "timeControl.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )

{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "dgTransform", dgTransform::id, dgTransform::creator,
								  dgTransform::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "retargetBlender", retargetBlender::id, retargetBlender::creator,
								  retargetBlender::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "udAttrBlender", udAttrBlender::id, udAttrBlender::creator,
								  udAttrBlender::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "retargetOrientNode", retargetOrientNode::id, retargetOrientNode::creator,
								  retargetOrientNode::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "retargetTransNode", retargetTransNode::id, retargetTransNode::creator,
								  retargetTransNode::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "editMatrixByCurve", editMatrixByCurve::id, editMatrixByCurve::creator,
								  editMatrixByCurve::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "transRotateCombineMatrix", transRotateCombineMatrix::id, transRotateCombineMatrix::creator,
								  transRotateCombineMatrix::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "retargetLocator", retargetLocator::id, retargetLocator::creator,
								  retargetLocator::initialize, MPxNode::kLocatorNode );
    CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "meshShapeLocator", meshShapeLocator::id, meshShapeLocator::creator,
								  meshShapeLocator::initialize, MPxNode::kLocatorNode );
    CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "timeControl", timeControl::id, timeControl::creator,
								  timeControl::initialize );
    CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( dgTransform::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( retargetBlender::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( udAttrBlender::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( retargetOrientNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( retargetTransNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( editMatrixByCurve::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( transRotateCombineMatrix::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( retargetLocator::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( meshShapeLocator::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = plugin.deregisterNode( timeControl::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	return status;
}
