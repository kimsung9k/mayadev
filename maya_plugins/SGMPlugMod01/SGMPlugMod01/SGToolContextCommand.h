#pragma once

#include "SGBase.h"
#include <maya/MStatus.h>
#include <maya/MString.h>
#include <maya/MPxContextCommand.h>
#include "SGToolContext.h"

class SGToolContextCommand : public MPxContextCommand
{
public:
	SGToolContextCommand();
	virtual ~SGToolContextCommand();
	static void* creator();

	virtual MStatus doEditFlags();
	virtual MStatus doQueryFlags();
	virtual MStatus appendSyntax();
	virtual MPxContext* makeObj();

	SGToolContext* m_pContext;
};