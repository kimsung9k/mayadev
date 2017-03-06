#ifndef _deleteBlendMeshInfo_h
#define _deleteBlendMeshInfo_h

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



struct  blendMeshInfo
{
	bool      existInputMesh;
	MString   nameConnectedNode;
	MString   nameConnectedAttr;

	MIntArray	 indicesDelta;
	MPointArray	 pointsDelta;

	MIntArray	 indicesTargetWeight;
	MFloatArray	 floatArrTargetWeight;

	MString   nameMesh;

	MIntArray		indicesMatrix;
	MObjectArray	oArrMatrix;

	MObject    oAnimCurve;
};


class	deleteBlendMeshInfo : public MPxCommand
{
public:
				deleteBlendMeshInfo();
	virtual		~deleteBlendMeshInfo();

	MStatus		doIt( const MArgList& args );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable()	const;

	static	MSyntax	newSyntax();

	static		void* creator();

	MStatus		getIndexInfo( blendMeshInfo& info, MObject oNode, int index );
	MStatus		setIndexInfo( blendMeshInfo& info, MObject oNode, int index );

public:
	MDGModifier m_mdgModifier;
	MDGModifier m_deleteModifier;

	int  m_indexTarget;
	int  m_indexLast;
	MObject  m_oNode;

	blendMeshInfo  m_infoTarget;
	blendMeshInfo  m_infoLast;
};

#endif