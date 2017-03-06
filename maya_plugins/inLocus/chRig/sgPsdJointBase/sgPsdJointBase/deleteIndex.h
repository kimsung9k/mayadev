#ifndef _deleteIndex_h
#define _deleteIndex_h


#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>

#include <maya/MSelectionList.h>

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

#include <maya/MString.h>


class DeleteIndex : MPxCommand
{
public:
	DeleteIndex();
	virtual ~DeleteIndex();

	MStatus doIt( const MArgList& args );
	MStatus redoIt();
	MStatus undoIt();
	bool isUndoable() const;

	static MSyntax newSyntax();
	static void* creator();

public:
	MObject  m_oNode;
	int      m_indexTarget;
	MPlug    m_plugTarget;
	MString     m_namePlug;

	MString  m_shapeName;
	float    m_weight;
	MPointArray m_deltas;
	MIntArray   m_logicalIndices;
	
};


#endif