#ifndef _CreateJointContextCommand_h
#define _CreateJointContextCommand_h

#include <maya/MPxContextCommand.h>
#include "CreateJointContext.h"

class CreateJointContextCommand : public MPxContextCommand
{
public:
	CreateJointContextCommand();
	virtual ~CreateJointContextCommand();
	static void* creator();

	virtual MStatus doEditFlags();
	virtual MStatus doQueryFlags();
	virtual MStatus appendSyntax();
	virtual MPxContext* makeObj();

	CreateJointContext* m_pContext;
};

#endif