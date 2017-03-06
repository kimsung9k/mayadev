#ifndef _sgCurveDraw_contextCommand_h
#define _sgCurveDraw_contextCommand_h

#include <maya/MPxContextCommand.h>
#include "sgCurveDraw_context.h"

class sgCurveDraw_contextCommand : public MPxContextCommand
{
public:
	sgCurveDraw_contextCommand();
	virtual ~sgCurveDraw_contextCommand();
	static void* creator();

	virtual MStatus doEditFlags();
	virtual MStatus doQueryFlags();
	virtual MStatus appendSyntax();
	virtual MPxContext* makeObj();

	sgCurveDraw_context* m_pContext;
};

#endif