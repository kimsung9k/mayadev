#ifndef _buildSkin_h
#define _buildSkin_h

#include <maya/MFnMessageAttribute.h>

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
#include <maya/MItDependencyGraph.h>

#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MFnMatrixData.h>

#include <maya/MFnMesh.h>
#include <maya/MFnTransform.h>

#include <maya/MDagPath.h>

#include <maya/MFnAttribute.h>

#include <maya/M3dView.h>
#include <maya/MGlobal.h>
#include <maya/MDGModifier.h>
#include <maya/MDagModifier.h>

#include <maya/MString.h>

#include <vector>

using namespace std;

class	buildSkinMesh : public MPxCommand
{
public:
				buildSkinMesh();
	virtual		~buildSkinMesh();

	MStatus		doIt( const MArgList& args );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable()	const;

	static	MSyntax	newSyntax();

	static		void* creator();

	MStatus  displayError();

	MStatus  getNodes( MDagPath& path,
		               MFnDependencyNode& fnSkinCluster, 
					   MFnDependencyNode& fnBlendAndFixedShape );
	MStatus  buildOriginalMesh( MFnTransform& trParent );
	MStatus  getMatrixArrays();
	MStatus  getWeightInfos();
	MStatus  getDeltaInfos();
	MStatus	 buildTarget();
	MStatus  buildInverse();
	MStatus  connect();

public:
	M3dView      m_view;
	MDagModifier m_mdagModifier;
	MDGModifier  m_mdgModifier;

	MSelectionList   m_selectionBefore;
	MDagPath m_pathTarget;
	MString m_nameIndex;

	int  m_index;
	int  m_numVertices;
	MFnDependencyNode m_fnSkinCluster;
	MFnDependencyNode m_fnInverseNode;
	MFnDependencyNode m_fnBlendAndFixedShape;
	MFnTransform      m_trTargetParent;
	MFnTransform      m_trInverseParent;
	MFnMesh           m_meshTargetChild;
	MFnMesh           m_meshInverseChild;

	MIntArray         m_intArrMapping;
	MPointArray       m_pointArrDelta;

	MMatrix m_mtxWorld;
	MMatrix m_mtxInverse;
	MIntArray    m_intArrBuildLogical;
	MMatrixArray m_mtxArrBuild;
	MMatrixArray m_mtxArrMatrix;
	MMatrixArray m_mtxArrBindPre;

	MPlug m_plugInput;
	MPlug m_plugOutput;
	
	vector< MIntArray >   m_vIntArrIndices;
	vector< MFloatArray > m_vFloatArrValues;
};

#endif