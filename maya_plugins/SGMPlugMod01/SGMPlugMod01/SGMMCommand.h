#pragma once

#include <SGBase.h>
#include <maya/MStatus.h>
#include <maya/MObject.h>
#include <maya/MSelectionList.h>
#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MSyntax.h>


class QMouseEvent;

class SGMMCommand : public MPxCommand
{
public:
	SGMMCommand();
	virtual ~SGMMCommand();
	static void* creator();
	static MSyntax newSyntax();

	bool m_psm;

	virtual MStatus doIt(const MArgList& args);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;

	static MString commandName;
};