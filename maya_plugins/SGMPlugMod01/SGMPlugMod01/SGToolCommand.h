#pragma once

#include "SGBase.h"
#include <maya/MStatus.h>
#include <maya/MObject.h>
#include <maya/MSelectionList.h>
#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MSyntax.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MIntArray.h>
#include "SGSelection.h"
#include "SGDataType.h"


class QMouseEvent;

class SGToolCommand : public MPxCommand
{
public:
	SGToolCommand();
	virtual ~SGToolCommand();
	static void* creator();
	static MSyntax newSyntax();

	virtual MStatus doIt(const MArgList& args);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;
	static void clearResult();

	static MString commandName;

	bool m_isVm;
	bool m_isPs;
	bool m_isPsp;
	bool m_isDel;
	bool m_isSel;
	bool m_isPsr;

	MDagPath     m_dagPathMesh;
	MPointArray  m_vmPointsBefore;
	MPointArray  m_vmPointsAfter;
	MIntArray    m_vmMergeIndices;

	static MDagPath     dagPathMesh;
	static MPointArray  vmPoints_before;
	static MPointArray  vmPoints_after;
	static MIntArray    vmMergeIndices;

	MIntArray   m_psIndices;
	MFloatArray m_psParams;

	splitPoint m_beforeSpPoint;
	splitPoint m_afterSpPoint;
	static splitPoint beforeSpPoint;
	static splitPoint afterSpPoint;

	static MIntArray   psIndices;
	static MFloatArray psParams;

	MIntArray m_delEdgeIndices;
	MIntArray m_delPolyIndices;

	static MIntArray delEdgeIndices;
	static MIntArray delPolyIndices;

	vector<SGSelection> m_selBefore;
	vector<SGSelection> m_selAfter;
	static vector<SGSelection> selBefore;
	static vector<SGSelection> selAfter;

	vector<int>   m_rootEdges;
	vector<float> m_rootWeights;
	vector<MIntArray> m_indicesEdges;
	static vector<int> rootEdges;
	static vector<float> rootWeights;
	static vector<MIntArray> indicesEdges;

	void mergeVertex();
	bool setPntsZero(MPlug plugPnts, MIntArray& indices, MPointArray& pnts);
	MPlug getCurrentMeshOutputConnection(MObject oMesh);
	MObject addNewNodeOnMesh(MObject oMesh, MString nodeType, 
		MString nodeInputName, MString nodeOutputName);
	void pushSplitPoint();
	void polySplit(const MIntArray& edgeIndices, const MFloatArray& edgeParams);
	void polySplitRing(int rootEdge, float rootWeight, MIntArray& indicesEdge);
	MStatus deleteBeforeNode(MDagPath dagPath, MString nodeName, MString inputName);
	void deleteComponent(MDagPath dagPath, MIntArray edgeIndices, MIntArray polyIndices);
};