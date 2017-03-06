#include "retargetingCommand.h"
#include "ExportImportPose.h"
#include <maya/MFnPlugin.h>



MStatus initializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj, "Locus", "2014", "Any");

	status = plugin.registerCommand( "retargetingCommand", RetargetingCommand::creator, RetargetingCommand::newSyntax );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSceneMessage msg;
	RetargetingCommand::m_callbackId = msg.addCallback( MSceneMessage::kBeforeOpen, RetargetingCommand::clearCtlSet );

	return status;
}


MStatus uninitializePlugin( MObject obj )
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterCommand( "retargetingCommand" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSceneMessage msg;
	msg.removeCallback( RetargetingCommand::m_callbackId );

	return status;
}