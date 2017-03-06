#include "sgCurveEditBrush_contextCommand.h"

sgCurveEditBrush_contextCommand::sgCurveEditBrush_contextCommand()
{
	m_pContext = NULL;
}


sgCurveEditBrush_contextCommand::~sgCurveEditBrush_contextCommand()
{
	if( m_pContext != NULL )
		delete m_pContext;
}


void* sgCurveEditBrush_contextCommand::creator()
{
	return new sgCurveEditBrush_contextCommand();
}


MPxContext* sgCurveEditBrush_contextCommand::makeObj()
{
	m_pContext = new sgCurveEditBrush_context();
	return m_pContext;
}


MStatus sgCurveEditBrush_contextCommand::appendSyntax()
{
	MStatus status;
	MSyntax mSyntax = syntax();

	mSyntax.addFlag( "ron", "radiusEditOn", MSyntax::kBoolean );

	return MS::kSuccess;
}


MStatus sgCurveEditBrush_contextCommand::doEditFlags()
{
	MStatus status;
	MArgParser argData = parser();

	bool radiusEditOn;
	status = argData.getFlagArgument( "ron", 0, radiusEditOn );
	if( status ) m_pContext->m_radiusEditOn = radiusEditOn;

	return MS::kSuccess;
}


MStatus sgCurveEditBrush_contextCommand::doQueryFlags()
{
	MStatus status;
	return MS::kSuccess;
}