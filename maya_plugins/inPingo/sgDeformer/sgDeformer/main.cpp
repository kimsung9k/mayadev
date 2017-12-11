
#include <maya/MFnPlugin.h>
#include "sgFootPrintDeformer.h"


MStatus initializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin plugin(obj, "sg", "2017", "Any");
	plugin.registerNode(sgFootPrintDeformer::deformerName, sgFootPrintDeformer::id,
		sgFootPrintDeformer::creator, sgFootPrintDeformer::initialize );

	return MS::kSuccess;
}


MStatus uninitializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin plugin(obj);
	status = plugin.deregisterNode(sgFootPrintDeformer::id);

	return MS::kSuccess;
}