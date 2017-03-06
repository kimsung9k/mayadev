//#include "blendShapeFixNode.h"
#include "blendAndFixedShape.h"
#include "inverseSkinCluster.h"
#include "deleteBlendMeshInfo.h"
#include "assignBlendMeshInfo.h"
#include "addMirrorBlendMeshInfos.h"
#include "buildSkinMesh.h"
#include "vectorWeight.h"

#include <maya/MFnPlugin.h>


MStatus initializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2013", "Any");

	status = plugin.registerNode( "blendAndFixedShape", blendAndFixedShape::id, blendAndFixedShape::creator,
								  blendAndFixedShape::initialize, MPxNode::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "inverseSkinCluster", inverseSkinCluster::id, inverseSkinCluster::creator,
								  inverseSkinCluster::initialize, MPxNode::kDeformerNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerCommand( "deleteBlendMeshInfo", 
		                              deleteBlendMeshInfo::creator, deleteBlendMeshInfo::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerCommand( "assignBlendMeshInfo", 
		                              assignBlendMeshInfo::creator, assignBlendMeshInfo::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.registerCommand( "addMirrorBlendMeshInfos", 
		                              addMirrorBlendMeshInfos::creator, addMirrorBlendMeshInfos::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.registerCommand( "buildSkinMesh", 
		                              buildSkinMesh::creator, buildSkinMesh::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.registerNode( "vectorWeight", 
		vectorWeight::id, vectorWeight::creator, vectorWeight::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	/*
	status = plugin.registerNode( "angleDriver", angleDriver::id, angleDriver::creator,
								  angleDriver::initialize );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	*/
	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( blendAndFixedShape::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( inverseSkinCluster::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterCommand( "deleteBlendMeshInfo" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterCommand( "assignBlendMeshInfo" );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.deregisterCommand( "addMirrorBlendMeshInfos" );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	status = plugin.deregisterCommand( "buildSkinMesh" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( vectorWeight::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	/*
	status = plugin.deregisterNode( angleDriver::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	*/
	return status;
}
