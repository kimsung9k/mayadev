#include "precompile.h"

#include "SGToolContextCommand.h"


SGToolContextCommand::SGToolContextCommand()
{
	m_pContext = NULL;
}


SGToolContextCommand::~SGToolContextCommand()
{
	if (m_pContext != NULL)
		delete m_pContext;
}


void* SGToolContextCommand::creator()
{
	return new SGToolContextCommand();
}


MPxContext* SGToolContextCommand::makeObj()
{
	m_pContext = new SGToolContext();
	return m_pContext;
}


MStatus SGToolContextCommand::appendSyntax()
{
	MStatus status;
	return MS::kSuccess;
}


MStatus SGToolContextCommand::doEditFlags()
{
	MStatus status;
	MArgParser argData = parser();

	return MS::kSuccess;
}


MStatus SGToolContextCommand::doQueryFlags()
{
	MStatus status;
	return MS::kSuccess;
}