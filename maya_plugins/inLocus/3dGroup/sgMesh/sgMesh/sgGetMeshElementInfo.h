#ifndef _sgGetMeshElementInfo_h
#define _sgGetMeshElementInfo_h


#include <maya/MObject.h>
#include <maya/MGlobal.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <maya/MSelectionList.h>
#include <maya/MPxCommand.h>

#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnMesh.h>

#include <maya/MBoundingBox.h>

#include "sgBuildMeshData.h"


class sgGetMeshElementInfo : public MPxCommand
{
public:
	sgGetMeshElementInfo();
	virtual ~sgGetMeshElementInfo();

	static void*   creator();
	static MSyntax newSyntax();

	MStatus doIt( const MArgList& argList );
	MStatus redoIt();
	MStatus undoIt();
	bool    isUndoable() const;

	MStatus getInfomationFromSelection();

	static sgBuildMeshData_array   m_buildMeshDatas;

private:
	MSelectionList    m_selList;
};


#endif