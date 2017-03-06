#ifndef _addIndex_h
#define _addIndex_h


#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>

#include <maya/MSelectionList.h>

#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MObjectArray.h>
#include <maya/MFnDagNode.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>

#include <maya/MString.h>

#include <maya/MFnAttribute.h>

#include <maya/MGlobal.h>
#include <maya/MDGModifier.h>
#include <maya/MItDependencyGraph.h>

#include <maya/MString.h>


class AddIndex : MPxCommand
{
public:
	AddIndex();
	virtual ~AddIndex();

	MStatus doIt( const MArgList& args );
	MStatus redoIt();
	MStatus undoIt();
	bool isUndoable() const;

	static MSyntax newSyntax();
	static void* creator();

	MStatus		getShapeNode( MDagPath& path );
	MStatus     getDeformer();
	MStatus     getSkinInfo();

public:
	MObject  m_oDeformer;

	MPlug    m_plugDeltaInfo;
	int      m_indexAdd;
};


#endif