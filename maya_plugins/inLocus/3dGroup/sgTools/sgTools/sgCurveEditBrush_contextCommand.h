#ifndef _sgCurveEditBrush_contextCommand_h
#define _sgCurveEditBrush_contextCommand_h

#include <maya/MPxContextCommand.h>
#include "sgCurveEditBrush_context.h"

class sgCurveEditBrush_contextCommand : public MPxContextCommand
{
public:
	sgCurveEditBrush_contextCommand();
	virtual ~sgCurveEditBrush_contextCommand();
	static void* creator();

	virtual MStatus doEditFlags();
	virtual MStatus doQueryFlags();
	virtual MStatus appendSyntax();
	virtual MPxContext* makeObj();

	sgCurveEditBrush_context* m_pContext;
};

#endif