#pragma once

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

#include <SGBase.h>
#include <SGSelection.h>
#include <SGSplitPoint.h>
#include <SGMesh.h>


class QMouseEvent;

class SGCommand : public MPxCommand
{
public:
	SGCommand();
	virtual ~SGCommand();
	static void* creator();
	static MSyntax newSyntax();

	virtual MStatus doIt(const MArgList& args);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	bool    isUndoable() const;
	static void clearResult();

	bool m_isSt;
	bool m_isVm;
	bool m_isDel;
	bool m_isUpm;
	bool m_isUpc;
	bool m_isPntsZero;
	long m_isSym;
	long m_isTm;
	bool m_getOption;

	bool m_undoableValue;

	MStringArray m_stResults;

	MDagPath     m_dagPathMesh;
	MPointArray  m_vmPointsBefore;
	MPointArray  m_vmPointsAfter;
	MIntArray    m_vmMoveIndices;
	MIntArray    m_vmMergeIndices;

	static MDagPath     dagPathMesh;
	static MPointArray  vmPoints_before;
	static MPointArray  vmPoints_after;
	static MIntArray    vmMoveIndices;
	static MIntArray    vmMergeIndices;

	vector<MIntArray>   m_psIndices;
	vector<MFloatArray> m_psParams;
	vector<MPointArray> m_psPoints;
	static vector<MIntArray>   psIndices;
	static vector<MFloatArray> psParams;
	static vector<MPointArray> psPoints;

	MIntArray m_delEdgeIndices;
	MIntArray m_delPolyIndices;
	static MIntArray delEdgeIndices;
	static MIntArray delPolyIndices;

	vector<int>   m_rootEdges;
	vector<float> m_rootWeights;
	vector<MIntArray> m_indicesEdges;
	static vector<int> rootEdges;
	static vector<float> rootWeights;
	static vector<MIntArray> indicesEdges;

	MIntArray m_bvlIndices;
	double m_bvlOffset;
	static MIntArray bvlIndices;
	static double bvlOffset;

	void mergeVertex();
	void deleteComponent(MDagPath dagPath, MIntArray edgeIndices, MIntArray polyIndices);
	void polySplit( const vector<MIntArray>& indices, const vector<MFloatArray>& params, const vector<MPointArray>& points);
	void polySplitRing(int rootEdge, float rootWeight, MIntArray& indicesEdge);

	bool checkMeshIsSelected();
};