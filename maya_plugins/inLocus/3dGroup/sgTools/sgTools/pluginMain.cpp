#include "CreateJointContext.h"
#include "CreateJointContextCommand.h"
#include "sgCurveEditBrush_contextCommand.h"
#include "sgCurveEditBrush_manip.h"
#include "sgCurveDraw_contextCommand.h"

#include <maya/MFnPlugin.h>

char contextCommandName[30] = "createJointContext";
char toolCommandName[30]    = "createJointTool";

MStatus initializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin plugin( obj, "sggim", "1.0", "Any" );


	status = plugin.registerNode( "sgCurveEditBrush_manip", sgCurveEditBrush_manip::id,
		sgCurveEditBrush_manip::creator, sgCurveEditBrush_manip::initialize, MPxNode::kManipContainer );


	status = plugin.registerContextCommand( contextCommandName,
		                                    CreateJointContextCommand::creator,
											toolCommandName,
											CreateJointToolCommand::creator );
	CHECK_MSTATUS_AND_RETURN_IT( status );


	char buffer[512];
	sprintf( buffer, "%s %s1", contextCommandName, contextCommandName );
	cout << contextCommandName << " : is loaded" << endl;
	MGlobal::executeCommand( buffer );

	status = plugin.registerContextCommand( "sgCurveEditBrushContext",
		sgCurveEditBrush_contextCommand::creator,
		"sgCurveEditBrushTool",
		sgCurveEditBrush_ToolCommand::creator );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	sprintf( buffer, "%s %s1", "sgCurveEditBrushContext", "sgCurveEditBrushContext" );
	MGlobal::executeCommand( buffer );

	status = plugin.registerContextCommand( "sgCurveDrawContext",
		sgCurveDraw_contextCommand::creator,
		"sgCurveDrawTool",
		sgCurveDraw_ToolCommand::creator );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	sprintf( buffer, "%s %s1", "sgCurveDrawContext", "sgCurveDrawContext" );
	MGlobal::executeCommand( buffer );

    return MS::kSuccess;
}


MStatus uninitializePlugin( MObject obj )
{
    MStatus status;

    MFnPlugin plugin( obj );

	char buffer[512];

	sprintf( buffer, "deleteUI %s1", contextCommandName );
	MGlobal::executeCommand( buffer );

	sprintf( buffer, "deleteUI %s1", "sgCurveEditBrushContext" );
	MGlobal::executeCommand( buffer );

	sprintf( buffer, "deleteUI %s1", "sgCurveDrawContext" );
	MGlobal::executeCommand( buffer );

	status = plugin.deregisterContextCommand( contextCommandName, toolCommandName );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterContextCommand( "sgCurveEditBrushContext", "sgCurveEditBrushTool" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterContextCommand( "sgCurveDrawContext", "sgCurveDrawTool" );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = plugin.deregisterNode( sgCurveEditBrush_manip::id );
	CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}