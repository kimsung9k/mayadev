#include "CreateJointContextCommand.h"

CreateJointContextCommand::CreateJointContextCommand()
{
	m_pContext = NULL;
}


CreateJointContextCommand::~CreateJointContextCommand()
{
	if( m_pContext != NULL )
		delete m_pContext;
}


void* CreateJointContextCommand::creator()
{
	return new CreateJointContextCommand();
}


MPxContext* CreateJointContextCommand::makeObj()
{
	m_pContext = new CreateJointContext();
	return m_pContext;
}


MStatus CreateJointContextCommand::appendSyntax()
{
	MStatus status;



	return MS::kSuccess;
}


MStatus CreateJointContextCommand::doEditFlags()
{
	MStatus status;
	MArgParser argData = parser();

	return MS::kSuccess;
}


MStatus CreateJointContextCommand::doQueryFlags()
{
	MStatus status;
	return MS::kSuccess;
}