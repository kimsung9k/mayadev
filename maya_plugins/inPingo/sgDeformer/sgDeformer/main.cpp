
#include <maya/MFnPlugin.h>
#include "sgFootPrintMesh.h"
#include "sgModifiedMeshKeeper.h"
#include "sgBulgeDeformer.h"
#include "sgSnowBulge.h"


MStatus initializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin plugin(obj, "sg", "2017", "Any");
	plugin.registerNode(sgFootPrintMesh::deformerName, sgFootPrintMesh::id,
		sgFootPrintMesh::creator, sgFootPrintMesh::initialize, sgFootPrintMesh::kDeformerNode);

	plugin.registerNode(sgModifiedMeshKeeper::nodeName, sgModifiedMeshKeeper::id,
		sgModifiedMeshKeeper::creator, sgModifiedMeshKeeper::initialize);

	plugin.registerNode(sgSnowBulge::nodeName, sgSnowBulge::id,
		sgSnowBulge::creator, sgSnowBulge::initialize);

	plugin.registerNode(sgBulgeDeformer::nodeName, sgBulgeDeformer::id,
		sgBulgeDeformer::creator, sgBulgeDeformer::initialize, sgBulgeDeformer::kDeformerNode );

	return MS::kSuccess;
}


MStatus uninitializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin plugin(obj);
	status = plugin.deregisterNode(sgFootPrintMesh::id);

	status = plugin.deregisterNode(sgModifiedMeshKeeper::id);

	status = plugin.deregisterNode(sgSnowBulge::id);

	status = plugin.deregisterNode(sgBulgeDeformer::id);

	return MS::kSuccess;
}