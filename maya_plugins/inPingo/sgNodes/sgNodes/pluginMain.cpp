#include "SGControlledCurve00.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, "Pingo", "2017", "Any");

	status = plugin.registerNode(SGControlledCurve00::typeName, SGControlledCurve00::id, SGControlledCurve00::creator,
		SGControlledCurve00::initialize);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);

	status = plugin.deregisterNode(SGControlledCurve00::id);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;
}
