#ifndef _assignBlendMeshInfo_h
#define _assignBlendMeshInfo_h

#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>

#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>

#include <maya/MObject.h>
#include <maya/MFnDagNode.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>

#include <maya/MString.h>

#include <maya/MFnAttribute.h>

#include <maya/MGlobal.h>
#include <maya/MDGModifier.h>

#include <maya/MString.h>


class	assignBlendMeshInfo : public MPxCommand
{
public:
				assignBlendMeshInfo();
	virtual		~assignBlendMeshInfo();

	MStatus		doIt( const MArgList& args );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable()	const;

	static	MSyntax	newSyntax();

	static		void* creator();
	MStatus		getShapeNode( MDagPath& path );

public:
	MDGModifier m_mdgModifier;

	int  m_indexTarget;
	MDagPath  m_pathShape;
	MObject  m_oNode;
};

#endif