#include "precompile.h"

#include "SGToolContextCommand.h"
#include "SGCommand.h"
#include "SGMMCommand.h"
#include "Names.h"
#include <SGBase.h>
#include <SGManip.h>

#include <maya/MFnPlugin.h>
#include <SGPrintf.h>

MStatus initializePlugin(MObject obj)
{
	sgPrintf("initialize plugin");
	MStatus status;
	MFnPlugin plugin(obj, "sggim", "1.0", "Any");

	status = plugin.registerNode(Names::manipName, SGManip::id,
		SGManip::creator, SGManip::initialize, MPxNode::kManipContainer );

	plugin.registerContextCommand(Names::contextName,
		SGToolContextCommand::creator);
	plugin.registerCommand(Names::commandName,
		SGCommand::creator);

	SGExecuteCommand( false, "%s %s", Names::contextName.asChar(), Names::toolName.asChar() );

	return MS::kSuccess;
}


MStatus uninitializePlugin(MObject obj)
{
	MStatus status;
	MFnPlugin plugin(obj);

	SGExecuteCommand(false, "deleteUI %s", Names::toolName.asChar());

	plugin.deregisterContextCommand(Names::contextName);
	plugin.deregisterCommand(Names::commandName);

	plugin.deregisterNode(SGManip::id);

	return MS::kSuccess;
}