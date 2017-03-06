#include "node.h"
#include "addIndex.h"
#include "deleteIndex.h"
#include "addShape.h"
#include <maya/MFnPlugin.h>



MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2014", "Any");

	status = plugin.registerNode( "psdJointBase", MainNode::id,
		MainNode::creator, MainNode::initialize, MainNode::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerCommand( "psdJointBase_addIndex", AddIndex::creator, AddIndex::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerCommand( "psdJointBase_deleteIndex", DeleteIndex::creator, DeleteIndex::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerCommand( "psdJointBase_addShape", AddShape::creator, AddShape::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}



MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( MainNode::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterCommand( "psdJointBase_addIndex" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterCommand( "psdJointBase_deleteIndex" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterCommand( "psdJointBase_addShape" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return status;
}