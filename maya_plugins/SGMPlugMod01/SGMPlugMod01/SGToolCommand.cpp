#include "precompile.h"

#include "SGToolCommand.h"
#include "SGSpace.h"

#include <maya/M3dView.h>
#include <maya/MPlug.h>
#include <maya/MArgDatabase.h>
#include <maya/MPlugArray.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MFnComponentListData.h>

#include "SGMesh.h"


MString SGToolCommand::commandName = "SGMToolMod01Command";

MDagPath  SGToolCommand::dagPathMesh;
MPointArray SGToolCommand::vmPoints_before;
MPointArray SGToolCommand::vmPoints_after;
MIntArray   SGToolCommand::vmMergeIndices;

MIntArray   SGToolCommand::psIndices;
MFloatArray SGToolCommand::psParams;

splitPoint  SGToolCommand::beforeSpPoint;
splitPoint  SGToolCommand::afterSpPoint;

MIntArray   SGToolCommand::delEdgeIndices;
MIntArray   SGToolCommand::delPolyIndices;

vector<SGSelection> SGToolCommand::selBefore;
vector<SGSelection> SGToolCommand::selAfter;

vector<int> SGToolCommand::rootEdges;
vector<float> SGToolCommand::rootWeights;
vector<MIntArray> SGToolCommand::indicesEdges;


void SGToolCommand::clearResult() {
	SGToolCommand::vmPoints_before.clear();
	SGToolCommand::vmPoints_after.clear();
}

SGToolCommand::SGToolCommand() {
	m_isVm = false;
	m_isPs = false;
	m_isPsp = false;
	m_isDel = false;
	m_isSel = false;
	m_isPsr = false;
}

SGToolCommand::~SGToolCommand() {
}


void* SGToolCommand::creator() {
	return new SGToolCommand();
}


MSyntax SGToolCommand::newSyntax() {
	MSyntax syntax;

	syntax.addFlag("-vm", "-vtxMove", MSyntax::kNoArg);
	syntax.addFlag("-ps", "-polySplit", MSyntax::kNoArg);
	syntax.addFlag("-psp", "-pushSplitPoint", MSyntax::kNoArg);
	syntax.addFlag("-psr", "-polySplitRing", MSyntax::kNoArg);
	syntax.addFlag("-del", "-deleteComponent", MSyntax::kNoArg);
	syntax.addFlag("-sel", "-select", MSyntax::kNoArg);

	return syntax;
}


MStatus SGToolCommand::doIt(const MArgList& arg) {

	MStatus status;

	m_dagPathMesh = dagPathMesh;
	MString argStr = arg.asString(0);

	if (argStr == "-vm") m_isVm = true;
	if (argStr == "-ps") m_isPs = true;
	if (argStr == "-psp") m_isPsp = true;
	if (argStr == "-del") m_isDel = true;
	if (argStr == "-sel") m_isSel = true;
	if (argStr == "-psr") m_isPsr = true;

	if (m_isVm) {
		m_vmPointsBefore = vmPoints_before;
		m_vmPointsAfter = vmPoints_after;
		m_vmMergeIndices = vmMergeIndices;
		m_selBefore = selBefore;
		m_selAfter = selAfter;
	}
	else if (m_isPs) {
		m_psIndices = psIndices;
		m_psParams = psParams;
		m_selBefore = selBefore;
		m_selAfter = selAfter;
		m_beforeSpPoint = beforeSpPoint;
		m_afterSpPoint = afterSpPoint;
	}
	else if (m_isPsp) {
		m_beforeSpPoint = beforeSpPoint;
		m_afterSpPoint = afterSpPoint;
	}
	else if (m_isDel) {
		m_delEdgeIndices = delEdgeIndices;
		m_delPolyIndices = delPolyIndices;
		m_selBefore = selBefore;
		m_selAfter = selAfter;
	}
	else if (m_isSel) {
		m_selBefore = selBefore;
		m_selAfter  = selAfter;
	}
	else if (m_isPsr) {
		m_rootEdges = rootEdges;
		m_rootWeights = rootWeights;
		m_indicesEdges = indicesEdges;
		m_selBefore = selBefore;
		m_selAfter = selAfter;
	}

	vmPoints_before.clear();
	vmPoints_after.clear();
	vmMergeIndices.clear();
	psIndices.clear();
	psParams.clear();
	delEdgeIndices.clear();
	delPolyIndices.clear();

	return redoIt();
}

MStatus SGToolCommand::redoIt() {
	M3dView active3dView = M3dView().active3dView();
	MFnMesh fnMesh = m_dagPathMesh;

	SGMesh* pMesh = SGMesh::getMesh(m_dagPathMesh);

	if (m_isVm) {
		fnMesh.setPoints(m_vmPointsAfter, SGSpace::space);
		if (m_vmMergeIndices.length()) {
			SGToolCommand::mergeVertex();
		}
		fnMesh.updateSurface();
		active3dView.refresh(false, true);
		pMesh->update();
		if (m_vmMergeIndices.length()) {
			SGSelection::clearSelectionAll();
		}
		else {
			SGSelection::sels = m_selAfter;
		}
	}
	else if (m_isPs) {
		SGToolCommand::polySplit(m_psIndices, m_psParams);
		fnMesh.updateSurface();
		pMesh->update();
		active3dView.refresh(false, true);
		SGSelection::sels = m_selAfter;
		splitPoint::spPoints[1] = m_afterSpPoint;
	}
	else if (m_isPsp) {
		splitPoint::spPoints[1] = m_afterSpPoint;
	}
	else if (m_isDel) {
		if (m_delEdgeIndices.length() || m_delPolyIndices.length()) {
			SGToolCommand::deleteComponent(m_dagPathMesh, m_delEdgeIndices, m_delPolyIndices);
			fnMesh.updateSurface();
			pMesh->update();
		}
		else {
			for (int i = 0; i < m_selBefore.size(); i++) {
				if (m_selBefore[i].m_selIndices.length()) {
					if (m_selBefore[i].m_type == SGComponentType::kEdge)
						SGToolCommand::deleteComponent(m_selBefore[i].m_dagPath, m_selBefore[i].m_selIndices, MIntArray());
					else if (m_selBefore[i].m_type == SGComponentType::kPolygon)
						SGToolCommand::deleteComponent(m_selBefore[i].m_dagPath, MIntArray(), m_selBefore[i].m_selIndices);
					MFnMesh fnMeshSel = m_selBefore[i].m_dagPath;
					fnMeshSel.updateSurface();
					SGMesh* pMeshSel = SGMesh::getMesh(m_selBefore[i].m_dagPath);
					pMeshSel->update();
				}
			}
		}
		SGSelection::clearSelectionAll();
		active3dView.refresh(false, true);
	}
	else if (m_isSel) {
		SGSelection::sels = m_selAfter;
	}
	else if (m_isPsr) {
		for (int i = 0; i < m_rootEdges.size(); i++) {
			SGToolCommand::polySplitRing(m_rootEdges[i], m_rootWeights[i], m_indicesEdges[i]);
		}
		fnMesh.updateSurface();
		active3dView.refresh(false, true);
		pMesh->update();
		SGSelection::sels = m_selAfter;
	}
	MGlobal::executeCommand("select -cl");

	return MS::kSuccess;
}

MStatus SGToolCommand::undoIt() {

	SGMesh* pMesh = SGMesh::getMesh(m_dagPathMesh);
	M3dView active3dView = M3dView().active3dView();
	MFnMesh fnMesh = m_dagPathMesh;

	if (m_isVm) {
		if (m_vmMergeIndices.length()) {
			deleteBeforeNode(m_dagPathMesh, "polyMergeVert", "inputPolymesh");
		}
		fnMesh.setPoints(m_vmPointsBefore, SGSpace::space);
		fnMesh.updateSurface();
		active3dView.refresh(false, true);
		pMesh->update();
		SGSelection::sels = m_selBefore;
	}
	else if (m_isPs) {
		deleteBeforeNode(m_dagPathMesh, "polySplit", "inputPolymesh");
		if( m_psIndices.length() == 4 )deleteBeforeNode(m_dagPathMesh, "polySplit", "inputPolymesh");
		fnMesh.updateSurface();
		active3dView.refresh(false, true);
		pMesh->update();
		SGSelection::sels = m_selBefore;
		splitPoint::spPoints[1] = m_beforeSpPoint;
	}
	else if (m_isPsp) {
		splitPoint::spPoints[1] = m_beforeSpPoint;
	}
	else if (m_isDel) {
		if (m_delEdgeIndices.length() || m_delPolyIndices.length()) {
			if (m_delEdgeIndices.length())deleteBeforeNode(m_dagPathMesh, "polyDelEdge", "inputPolymesh");
			if (m_delPolyIndices.length())deleteBeforeNode(m_dagPathMesh, "deleteComponent", "inputGeometry");
			fnMesh.updateSurface();
			pMesh->update();
		}
		else {
			for (int i = 0; i < m_selBefore.size(); i++) {
				if (m_selBefore[i].m_selIndices.length()) {
					if (m_selBefore[i].m_type == SGComponentType::kEdge)
						deleteBeforeNode(m_selBefore[i].m_dagPath, "polyDelEdge", "inputPolymesh");
					else if (m_selBefore[i].m_type == SGComponentType::kPolygon)
						deleteBeforeNode(m_selBefore[i].m_dagPath, "deleteComponent", "inputGeometry");
					MFnMesh fnMeshSel = m_selBefore[i].m_dagPath;
					fnMeshSel.updateSurface();
					SGMesh* pMeshSel = SGMesh::getMesh(m_selBefore[i].m_dagPath);
					pMeshSel->update();
				}
			}
		}
		active3dView.refresh(false, true);
		SGSelection::sels = m_selBefore;
	}
	else if (m_isSel) {
		SGSelection::sels = m_selBefore;
	}
	else if (m_isPsr) {
		for (int i = 0; i < m_rootEdges.size(); i++) {
			deleteBeforeNode(m_dagPathMesh, "polySplitRing", "inputPolymesh");
		}
		fnMesh.updateSurface();
		active3dView.refresh(false, true);
		pMesh->update();
		SGSelection::sels = m_selBefore;
	}
	MGlobal::executeCommand("select -cl");
	return MS::kSuccess;
}


bool SGToolCommand::isUndoable() const {
	return true;
}