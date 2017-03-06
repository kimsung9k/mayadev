#include "sgCurveDraw_contextCommand.h"

sgCurveDraw_contextCommand::sgCurveDraw_contextCommand()
{
	m_pContext = NULL;
}


sgCurveDraw_contextCommand::~sgCurveDraw_contextCommand()
{
	if( m_pContext != NULL )
		delete m_pContext;
}


void* sgCurveDraw_contextCommand::creator()
{
	return new sgCurveDraw_contextCommand();
}


MPxContext* sgCurveDraw_contextCommand::makeObj()
{
	m_pContext = new sgCurveDraw_context();
	return m_pContext;
}


MStatus sgCurveDraw_contextCommand::appendSyntax()
{
	MStatus status;
	MSyntax mSyntax = syntax();

	mSyntax.addFlag( "em", "editMode", MSyntax::kBoolean );

	return MS::kSuccess;
}


MStatus sgCurveDraw_contextCommand::doEditFlags()
{
	MStatus status;
	MArgParser argData = parser();

	bool editMode;
	status = argData.getFlagArgument( "em", 0, editMode );
	m_pContext->m_editMode = editMode;

	return MS::kSuccess;
}


MStatus sgCurveDraw_contextCommand::doQueryFlags()
{
	MStatus status;
	return MS::kSuccess;
}