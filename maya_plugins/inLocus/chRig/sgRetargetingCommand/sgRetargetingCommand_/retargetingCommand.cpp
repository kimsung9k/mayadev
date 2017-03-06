#include "retargetingCommand.h"



     MString RetargetingCommand::m_nsSrc;
MStringArray RetargetingCommand::m_nsArrTrg;
        bool RetargetingCommand::m_srcNsUpdated;
         int RetargetingCommand::m_trgNsUpdated = -1;
        bool RetargetingCommand::m_srcMtxRequired;
		bool RetargetingCommand::m_srcRootRequired = true;
         int RetargetingCommand::m_trgMtxRequired = -1;
     CtlSet  RetargetingCommand::m_ctlSetSrc;
	 CtlSet  RetargetingCommand::m_ctlSetSrcFlip;
CtlSetArray  RetargetingCommand::m_ctlSetAnim;
CtlSetArray  RetargetingCommand::m_ctlSetAnimFlip;
CtlSetArray  RetargetingCommand::m_ctlSetArrTrgBase;
MCallbackId  RetargetingCommand::m_callbackId;

MFloatArray  RetargetingCommand::m_fArrFrame;



RetargetingCommand::RetargetingCommand()
{
	m_setAble = false;
	m_setCAnimAble = false;
	m_setEdited = false;
}



RetargetingCommand::~RetargetingCommand()
{}



void RetargetingCommand::clearCtlSet( void* data )
{
	m_nsSrc = "";
	m_srcNsUpdated = false;
	m_srcMtxRequired = false;
	m_nsArrTrg.clear();
	m_ctlSetArrTrgBase.setLength( 0 );
}



MStatus RetargetingCommand::doIt( const MArgList& argList )
{
	MStatus status;

	MArgDatabase argData( syntax(), argList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = argChk_exportImport( argData );
	if( status == MS::kSuccess )
	{
		retargetMethod = retargetType::fileType;
		return MS::kSuccess;
	}
	else if( status == MS::kFailure )
	{
		MGlobal::displayError( "File Trans is Failed" );
		return MS::kFailure;
	}

	arcChk_setClear( argData );
	argChk_getSelectionList( argData );
	argChk_setSrcWorldName( argData );
	argChk_setTrgWorldName( argData );
	argChk_getSrcMtxInfo( argData );
	argChk_getTrgMtxInfo( argData );
	argChk_setAble( argData );
	argChk_flip( argData );
	argChk_updateEachWeight( argData );
	argChk_updateWeight( argData );
	argChk_enable( argData );

	chk_matrixUpdate();


	return redoIt();
}



MStatus RetargetingCommand::redoIt()
{
	MStatus status;

	if( m_setAble )
	{
		if( m_srcMtxRequired ) return MS::kSuccess;
		retargetPose();
	}
	else if( m_setCAnimAble )
	{
		status = retargetCAnim();
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	return MS::kSuccess;
}



MStatus RetargetingCommand::undoIt()
{
	MStatus status;

	if( m_setEdited )
	{
		for( int i=0; i< m_ctlSetArrTrg.length(); i++ )
			m_ctlSetArrTrg[i].undoRetarget();
	}

	return MS::kSuccess;
}



bool RetargetingCommand::isUndoable() const
{
	if( retargetMethod == retargetType::setType || !m_setCAnimAble )
	{
		return true;
	}
	else
	{
		return false;
	}
}



void* RetargetingCommand::creator()
{
	RetargetingCommand* instance = new RetargetingCommand();
	return instance;
}



MSyntax RetargetingCommand::newSyntax()
{
	MSyntax syntax;

	syntax.addFlag( flagImport[0], flagImport[1], MSyntax::kBoolean );
	syntax.addFlag( flagExport[0], flagExport[1], MSyntax::kString );
	syntax.addFlag( flagImportCAnim[0], flagImportCAnim[1], MSyntax::kBoolean );
	syntax.addFlag( flagFileName[0], flagFileName[1], MSyntax::kString );

	syntax.addFlag( flagSrcWorld[0], flagSrcWorld[1], MSyntax::kBoolean ); 
	syntax.addFlag( flagTrgWorld[0], flagTrgWorld[1], MSyntax::kBoolean ); 
	syntax.addFlag( flagRetarget[0], flagRetarget[1], MSyntax::kBoolean );
	syntax.addFlag( flagRetargetAnim[0], flagRetargetAnim[1], MSyntax::kDouble );
	syntax.addFlag( flagWeight[0], flagWeight[1], MSyntax::kDouble );
	syntax.addFlag( flagClearAll[0], flagClearAll[1], MSyntax::kBoolean ); 
	syntax.addFlag( flagClearTarget[0], flagClearTarget[1], MSyntax::kBoolean );
	
	syntax.addFlag( flagFlip[0], flagFlip[1], MSyntax::kBoolean );

	syntax.addFlag( flagEnablePart[0], flagEnablePart[1], MSyntax::kString, MSyntax::kBoolean );
	syntax.addFlag( flagEnableCtl[0], flagEnableCtl[1], MSyntax::kString, MSyntax::kBoolean );
	syntax.addFlag( flagEnableFollow[0], flagEnableFollow[1], MSyntax::kString, MSyntax::kBoolean );

	syntax.addFlag( flagPartWeight[0], flagPartWeight[1], MSyntax::kString, MSyntax::kDouble );
	syntax.addFlag( flagCtlWeight[0],  flagCtlWeight[1],  MSyntax::kString, MSyntax::kDouble );

	syntax.setObjectType( MSyntax::kSelectionList );
	syntax.useSelectionAsDefault( true );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}