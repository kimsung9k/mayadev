#include "precompile.h"

#include "SGSelection.h"

#include "SGPrintf.h"
#include "SGMesh.h"
#include "SGSymmetry.h"
#include "SGIntersectResult.h"
#include "SGMatrix.h"
#include <maya/MSelectionList.h>
#include <maya/MRichSelection.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MBoundingBox.h>
#include <maya/MItSelectionList.h>
#include <maya/MFnSet.h>


SGSelection SGSelection::sels;


SGSelection::SGSelection() {
}


SGSelection::~SGSelection() {
}


SGSelection::SGSelection( const SGMesh* pMesh ) {
	this->pMesh = pMesh;
	clearSelection();
}


void SGSelection::updateFocusInfo(const vector<SGIntersectResult>& intersectResults) {
	m_beforeType = m_focusType;
	m_beforeIndex = m_focusIndex;
	m_focusIndex.resize(intersectResults.size());
	m_focusType.resize(intersectResults.size());
	for (int i = 0; i < intersectResults.size(); i++) {
		if (m_type[i] == SGComponentType::kVertex)
			m_focusIndex[i] = m_index[i];
		else if (m_type[i] == SGComponentType::kEdge)
			m_focusIndex[i] = m_index[i];
		else if (m_type[i] == SGComponentType::kPolygon)
			m_focusIndex[i] = m_index[i];
		m_focusType[i] = m_type[i];
	}
}


void SGSelection::select( const vector<SGIntersectResult>& intersectResults, int type) {
	SGComponentType resultType = intersectResults[0].resultType;

	if (resultType.isNone()) {return;}

	m_type.resize(intersectResults.size()); m_index.resize(intersectResults.size());
	for (int i = 0; i < intersectResults.size(); i++) {
		m_type[i]  = intersectResults[i].resultType;
		m_index[i] = intersectResults[i].resultIndex;
	}

	MString commandString = "select ";
	if (type == 1) {
		commandString += " -add ";
	}
	if (m_focusType.size() && m_type[0] != m_focusType[0] ) {
		commandString = "select -cl;" + commandString;
	}

	MFnMesh fnMesh = pMesh->dagPath;
	MString meshName = fnMesh.partialPathName();
	char buffer[512];

	for (unsigned int i = 0; i < intersectResults.size(); i++) {
		const SGIntersectResult& result = intersectResults[i];
		if (resultType == SGComponentType::kVertex)
			sprintf(buffer, " %s.vtx[%d] ", meshName.asChar(), result.vtxIndex );
		else if (resultType == SGComponentType::kEdge)
			sprintf(buffer, " %s.e[%d] ", meshName.asChar(), result.edgeIndex );
		else if (resultType == SGComponentType::kPolygon)
			sprintf(buffer, " %s.f[%d] ", meshName.asChar(), result.polyIndex );

		commandString += buffer;
	}
	commandString += ";";
	MGlobal::executeCommand(commandString, false, true );

	updateFocusInfo(intersectResults);
}



void SGSelection::addDBClickSelection(const vector<SGIntersectResult>& intersectResults)
{
	const SGComponentType& resultType = intersectResults[0].resultType;

	MFnMesh fnMesh( pMesh->dagPath );
	MString meshName = fnMesh.partialPathName();

	m_type.resize(2); m_index.resize(2);
	for (int i = 0; i < intersectResults.size(); i++) {
		m_type[i] = intersectResults[i].resultType;
		m_index[i] = intersectResults[i].resultIndex;
	}

	MString commandString = "select -add ";
	if (m_focusType.size() && m_type[0] != m_focusType[0]) {
		commandString = "select -cl;" + commandString;
	}

	int compLength;
	if (resultType == SGComponentType::kVertex)
		compLength = fnMesh.numVertices();
	else if (resultType == SGComponentType::kEdge)
		compLength = fnMesh.numEdges();
	else if (resultType == SGComponentType::kPolygon)
		compLength = fnMesh.numPolygons();

	MIntArray selIndicesMap = SGSelection::getMap( MIntArray(), compLength);

	for (unsigned int i = 0; i < intersectResults.size(); i++) {
		const SGIntersectResult& result = intersectResults[i];
		MIntArray resultIndices;
		SGComponentType beforeType = getBeforeType(i);
		int beforeIndex = getBeforeIndex(i);
		if (resultType != beforeType) {
			if (resultType == SGComponentType::kEdge)
				resultIndices = pMesh->getEdgeLoop(result.edgeIndex);
			for (unsigned int j = 0; j < resultIndices.length(); j++) 
				selIndicesMap[resultIndices[j]] = 1;
			continue;
		}

		if (resultType == SGComponentType::kVertex) {
			resultIndices = pMesh->getVertexLoop(result.vtxIndex, beforeIndex);
			for (unsigned int j = 0; j < resultIndices.length(); j++)
				selIndicesMap[resultIndices[j]] = 1;
		}
		else if (resultType == SGComponentType::kEdge) {
			MIntArray loopIndices = pMesh->getEdgeLoop(result.edgeIndex, beforeIndex);
			MIntArray ringIndices = pMesh->getEdgeRing(result.edgeIndex, beforeIndex);
			if ( !ringIndices.length() || loopIndices.length() < ringIndices.length())
				resultIndices = loopIndices;
			else
				resultIndices = ringIndices;

			for (unsigned int j = 0; j < resultIndices.length(); j++)
				selIndicesMap[resultIndices[j]] = 1;
		}
		else if (resultType == SGComponentType::kPolygon) {
			if (result.polyIndex == beforeIndex) {
			}
			else {
				resultIndices = pMesh->getPolygonLoop(result.polyIndex, beforeIndex);
			}
			for (unsigned int j = 0; j < resultIndices.length(); j++)
				selIndicesMap[resultIndices[j]] = 1;
		}
	}

	MString compString = "";
	if (resultType == SGComponentType::kVertex)
		compString = "vtx";
	else if (resultType == SGComponentType::kEdge)
		compString = "e";
	else if (resultType == SGComponentType::kPolygon)
		compString = "f";

	char buffer[512];
	for (unsigned int i = 0; i < selIndicesMap.length(); i++) {
		if (!selIndicesMap[i] ) continue;
		sprintf(buffer, " %s.%s[%d] ", meshName.asChar(), compString.asChar(), i);
		commandString += buffer;
	}

	commandString += ";";
	MGlobal::executeCommand(commandString, false, true);

	updateFocusInfo(intersectResults);
}



void SGSelection::dragSelection(const vector<SGIntersectResult>& intersectResults,
	const MPointArray& mousePoints, const MMatrix& camMatrix,
	const SGSymmetry& symInfo, int type) 
{
	m_type.resize(intersectResults.size()); m_index.resize(intersectResults.size());
	for (int i = 0; i < intersectResults.size(); i++) {
		m_type[i] = SGComponentType::kVertex;
	}

	MFnMesh fnMesh = pMesh->dagPath;
	MPointArray points;
	fnMesh.getPoints(points, MSpace::kWorld);

	MBoundingBox bb;
	for (unsigned int i = 0; i < mousePoints.length(); i++) {
		bb.expand(mousePoints[i]);
	}

	MMatrix worldToView = SGMatrix::getWorldToViewMatrix( camMatrix );
	MIntArray selMap = SGSelection::getMap(MIntArray(), fnMesh.numVertices());

	if (!SGBase::isolateVtxMap.length())
		SGBase::isolateVtxMap = SGSelection::getMap(MIntArray(), fnMesh.numVertices(), 1);

	for (unsigned int i = 0; i < points.length(); i++) {
		if (!SGBase::isolateVtxMap[i]) continue;
		MPoint viewPoint = SGMatrix::getViewPointFromWorld(points[i], camMatrix, &worldToView);
		if (!SGMatrix::isPointInPolygon2d(viewPoint, mousePoints, &bb)) continue;
		selMap[i] = 1;
		m_index[0] = i;
	}

	if (symInfo.isXMirror()) {
		MMatrix camMirrorMatrix = camMatrix * symInfo.mirrorMatrix();
		MMatrix worldToViewMirror = SGMatrix::getWorldToViewMatrix(camMirrorMatrix);

		for (unsigned int i = 0; i < points.length(); i++) {
			if (!SGBase::isolateVtxMap[i]) continue;
			MPoint viewPoint = SGMatrix::getViewPointFromWorld(points[i], camMirrorMatrix, &worldToViewMirror);
			if (!SGMatrix::isPointInPolygon2d(viewPoint, mousePoints, &bb)) continue;
			selMap[i] = 1;
			m_index[1] = i;
		}
	}

	MIntArray selIndices = getIndices(selMap);
	if (!selIndices.length()) {
		clearSelection();
		return;
	}

	MString commandString = "select ";
	if (type == 1) {
		commandString += " -add ";
	}
	else if (type == 2) {
		commandString += " -d ";
	}
	else if (type == 3) {
		commandString += " -cc ";
	}

	MString meshName = fnMesh.partialPathName();
	char buffer[512];

	for (unsigned int i = 0; i < selIndices.length(); i++) {
		sprintf(buffer, " %s.vtx[%d] ", meshName.asChar(), selIndices[i]);
		commandString += buffer;
	}
	commandString += ";";
	MGlobal::executeCommand(commandString, true, true);

	updateFocusInfo(intersectResults);
}



SGComponentType SGSelection::getBeforeType(int index)
{
	if ( m_beforeType.size() <= index) {
		return SGComponentType::kNone;
	}
	return m_beforeType[index];
}

int SGSelection::getBeforeIndex(int index)
{
	if (m_beforeType.size() <= index ) {
		return -1;
	}
	return m_beforeIndex[index];
}


void SGSelection::initialize(const SGMesh* pMesh) {
	this->pMesh = pMesh;
	m_type.clear();
	m_focusType.clear();
	m_focusIndex.clear();
	m_beforeType.clear();
	m_beforeIndex.clear();
}


void SGSelection::clearSelection()
{
	m_type.clear();
	m_focusType.clear();
	m_focusIndex.clear();
	m_beforeType.clear();
	m_beforeIndex.clear();
	MGlobal::executeCommand("select -cl;", false, true);
}



MPoint SGSelection::getComponentCenter( SGComponentType compType, int index) {

	MFnMesh fnMesh = pMesh->dagPath;
	MPoint center;

	if (compType == SGComponentType::kVertex) {
		fnMesh.getPoint(index, center, MSpace::kWorld);
	}
	else if (compType == SGComponentType::kEdge) {
		MIntArray vtxList = pMesh->getEdgeToVtxs(index);
		MPoint point1, point2;
		fnMesh.getPoint(vtxList[0], point1, MSpace::kWorld);
		fnMesh.getPoint(vtxList[1], point2, MSpace::kWorld);
		center = (point1 + point2) / 2;
	}
	else if (compType == SGComponentType::kPolygon) {
		MIntArray vtxList = pMesh->getPolyToVtxs(index);
		MBoundingBox bb;
		for (unsigned int i = 0; i < vtxList.length(); i++) {
			MPoint point;
			fnMesh.getPoint(vtxList[i], point, MSpace::kWorld);
			bb.expand(point);
		}
		center = bb.center();
	}
	return center;
}



MPoint SGSelection::getBeforeCenter() {
	if (!m_beforeType.size() || m_beforeIndex.size() ) return MPoint();
	return getComponentCenter(m_beforeType[0], m_beforeIndex[0]);
}


MPoint SGSelection::getFocusCenter() {
	if (!m_focusType.size() || !m_focusIndex.size() ) return MPoint();
	return getComponentCenter(m_focusType[0], m_focusIndex[0]);
}



MPoint SGSelection::getSelectionCenter( const SGSymmetry& symInfo) {
	MFnMesh fnMesh = pMesh->dagPath;
	MPoint focusPoint = getFocusCenter();

	if (m_focusIndex.size() && m_beforeIndex.size() ) {
		bool focusIsCenter = pMesh->isCenter(m_focusIndex[0], m_focusType[0]);
		bool beforeIsCenter = pMesh->isCenter(m_beforeIndex[0], m_beforeType[0]);
		if ( focusIsCenter && beforeIsCenter ) {
			focusPoint.x = 1;
		}
		else if ( focusIsCenter && !beforeIsCenter )
			focusPoint = getBeforeCenter();
	}

	MIntArray vtxIndices = getSelVtxIndices();
	MBoundingBox bb;

	MMatrix meshMatrix = pMesh->dagPath.inclusiveMatrix();
	MMatrix meshMatrixInv = pMesh->dagPath.inclusiveMatrixInverse();

	for (unsigned int i = 0; i < vtxIndices.length(); i++) {
		MPoint targetPoint;
		fnMesh.getPoint(vtxIndices[i], targetPoint, MSpace::kWorld);
		if (symInfo.compairIsMirror(focusPoint * meshMatrixInv, targetPoint * meshMatrixInv)) continue;
		bb.expand(targetPoint);
	}
	return bb.center();
}



bool SGSelection::selExists()
{
	if ( !m_focusType.size()) {
		return false;
	}
	return true;
}



bool SGSelection::selIsChanged(const MIntArray& map1, const MIntArray& map2)
{
	if (map1.length() != map2.length())  return true;
	for (unsigned int i = 0; i < map1.length(); i++) {
		if (map1[i] != map2[i]) return true;
	}
	return false;
}



bool SGSelection::growSelection() {
	MGlobal::executeCommand("GrowPolygonSelectionRegion;", false, true);
	return true;
}


bool SGSelection::reduceSelection() {
	MGlobal::executeCommand("ShrinkPolygonSelectionRegion;", false, true);
	return true;
}


MIntArray SGSelection::combineIndices(MIntArray indices1, MIntArray indices2, int maxNum )
{
	MIntArray indicesMap; indicesMap.setLength(maxNum);
	for (int i = 0; i < maxNum; i++) {
		indicesMap[i] = 0;
	}

	for (unsigned int i = 0; i < indices1.length(); i++) {
		indicesMap[indices1[i]] = 1;
	}
	for (unsigned int i = 0; i < indices2.length(); i++) {
		indicesMap[indices2[i]] = 1;
	}

	MIntArray indicesResult;
	for (int i = 0; i < maxNum; i++) {
		if (indicesMap[i])
			indicesResult.append(i);
	}
	return indicesResult;
}


MIntArray SGSelection::getSelVtxIndices()
{
	return SGSelection::getIndices( getSelVtxIndicesMap() );
}


MIntArray SGSelection::getSelEdgeIndices()
{
	return SGSelection::getIndices(getSelEdgeIndicesMap());
}


MIntArray SGSelection::getSelPolyIndices()
{
	return SGSelection::getIndices(getSelPolyIndicesMap());
}



MIntArray SGSelection::getSelVtxIndicesMap( )
{
	MIntArray selIndicesMap;

	MSelectionList selList;
	MGlobal::getActiveSelectionList(selList, true);

	selIndicesMap = getMap( MIntArray(), pMesh->numVertices );

	for (unsigned int i = 0; i < selList.length(); i++) {
		MDagPath targetPath;
		MObject  oComponent;
		selList.getDagPath(i, targetPath, oComponent);
		if ( !(targetPath == pMesh->dagPath )) continue;
		MFnSingleIndexedComponent singleComp = oComponent;
		MIntArray elements;
		singleComp.getElements(elements);

		if (MFn::kMeshVertComponent == singleComp.componentType()) {
			for (unsigned int j = 0; j < elements.length(); j++) {
				if (elements[j] >= pMesh->numVertices ) continue;
				selIndicesMap[elements[j]] = 1;
			}
		}

		if (MFn::kMeshEdgeComponent == singleComp.componentType()) {
			for (unsigned int j = 0; j < elements.length(); j++) {
				MIntArray vtxList = pMesh->getEdgeToVtxs(elements[j]);
				for (unsigned int k = 0; k < vtxList.length(); k++) {
					if (vtxList[k] >= pMesh->numVertices) continue;
					selIndicesMap[vtxList[k]] = 1;
				}
			}
		}

		if (MFn::kMeshPolygonComponent == singleComp.componentType()) {
			for (unsigned int j = 0; j < elements.length(); j++) {
				MIntArray vtxList = pMesh->getPolyToVtxs(elements[j]);
				for (unsigned int k = 0; k < vtxList.length(); k++) {
					if (vtxList[k] >= pMesh->numVertices) continue;
					selIndicesMap[vtxList[k]] = 1;
				}
			}
		}
	}

	return selIndicesMap;
}



MIntArray SGSelection::getSelEdgeIndicesMap()
{
	MIntArray selIndicesMap;

	MSelectionList selList;
	MGlobal::getActiveSelectionList(selList, true);

	selIndicesMap = getMap(MIntArray(), pMesh->numEdges);
	for (unsigned int i = 0; i < selList.length(); i++) {
		MDagPath targetPath;
		MObject  oComponent;
		selList.getDagPath(i, targetPath, oComponent);
		if (!(targetPath == pMesh->dagPath)) continue;
		MFnSingleIndexedComponent singleComp = oComponent;
		MIntArray elements;
		singleComp.getElements(elements);
		if (MFn::kMeshEdgeComponent != singleComp.componentType()) continue;
		for (unsigned int j = 0; j < elements.length(); j++) {
			selIndicesMap[elements[j]] = 1;
		}
	}
	return selIndicesMap;
}



MIntArray SGSelection::getSelPolyIndicesMap()
{
	MIntArray selIndicesMap;

	MSelectionList selList;
	MGlobal::getActiveSelectionList(selList, true);

	selIndicesMap = getMap(MIntArray(), pMesh->numVertices);
	for (unsigned int i = 0; i < selList.length(); i++) {
		MDagPath targetPath;
		MObject  oComponent;
		selList.getDagPath(i, targetPath, oComponent);
		if (!(targetPath == pMesh->dagPath)) continue;
		MFnSingleIndexedComponent singleComp = oComponent;
		MIntArray elements;
		singleComp.getElements(elements);
		if (MFn::kMeshPolygonComponent != singleComp.componentType()) continue;
		for (unsigned int j = 0; j < elements.length(); j++) {
			MIntArray vtxList = pMesh->getEdgeToVtxs(elements[j]);
			for (unsigned int k = 0; k < vtxList.length(); k++)
				selIndicesMap[vtxList[k]] = 1;
		}
	}
	return selIndicesMap;
}


MIntArray SGSelection::getSelIndicesMap(SGComponentType compType) {
	if (compType == SGComponentType::kVertex) {
		return getSelVtxIndicesMap();
	}
	else if (compType == SGComponentType::kEdge) {
		return getSelEdgeIndicesMap();
	}
	else if (compType == SGComponentType::kPolygon) {
		return getSelPolyIndicesMap();
	}
	return MIntArray();
}


MIntArray getSelectedSideEdges( const SGMesh* pMesh, int targetEdge, int beforeTarget, const MIntArray& indicesMap, MIntArray& checkedMap ) {
	checkedMap[targetEdge] = 1;
	MIntArray indicesEdges;
	MIntArray sideIndices = pMesh->getEdgeToEdges(targetEdge);
	for (unsigned int j = 0; j < sideIndices.length(); j++) {
		if (checkedMap[sideIndices[j]]) continue;
		if (sideIndices[j] == beforeTarget) continue;
		if (!indicesMap[sideIndices[j]]) continue;
		MIntArray newIndices = getSelectedSideEdges(pMesh,sideIndices[j], targetEdge, indicesMap, checkedMap);
		for (unsigned int k = 0; k < newIndices.length(); k++) {
			indicesEdges.append( newIndices[k] );
		}
	}
	indicesEdges.append(targetEdge);
	return indicesEdges;
}



vector<MIntArray> SGSelection::getEdgeLoopGroupByIndicesMap( const MIntArray& indicesMap )
{
	vector<MIntArray> edgeGroups;
	MIntArray checkedMap; checkedMap.setLength(indicesMap.length());
	for (unsigned int i = 0; i < checkedMap.length(); i++) {
		checkedMap[i] = 0;
	}

	for (unsigned int i = 0; i < indicesMap.length(); i++) {
		if (!indicesMap[i]) continue;
		if (checkedMap[i]) continue;
		MIntArray selGroup = getSelectedSideEdges( SGMesh::pMesh, i, -1, indicesMap, checkedMap);
		for (unsigned int j = 0; j < selGroup.length(); j++) {
			checkedMap[selGroup[j]] = 1;
		}
		edgeGroups.push_back(selGroup);
	}
	return edgeGroups;
}



MIntArray SGSelection::getMap(const MIntArray& indices, int maxLength, int defaultIndex, int setIndex) {
	MIntArray map; map.setLength(maxLength);
	for (unsigned int i = 0; i < map.length(); i++) {
		map[i] = defaultIndex;
	}
	for (unsigned int i = 0; i < indices.length(); i++) {
		map[indices[i]] = setIndex;
	}
	return map;
}


void SGSelection::setMap(MIntArray& map, const MIntArray& indices, int setIndex) {
	for (unsigned int i = 0; i < indices.length(); i++) {
		map[indices[i]] = setIndex;
	}
}


MIntArray SGSelection::getIndices(const MIntArray& map, int defaultIndex ) {
	MIntArray indices;
	for (unsigned int i = 0; i < map.length(); i++) {
		if (map[i] == defaultIndex) continue;
		indices.append(i);
	}
	return indices;
}



MFloatArray SGSelection::getVertexWeights() 
{
	MFloatArray vtxWeights;
	if (pMesh->dagPath.node().isNull()) return vtxWeights;
	MFnMesh fnMesh(pMesh->dagPath);
	vtxWeights.setLength(fnMesh.numVertices());
	for (unsigned int i = 0; i < vtxWeights.length(); i++) {
		vtxWeights[i] = 0;
	}

	int softSelectionExists;
	MGlobal::executeCommand("softSelect -q -sse ;", softSelectionExists, false, false);
	int symmetryOn =0;
	MGlobal::executeCommand("symmetricModelling -q -symmetry;", symmetryOn, false, false);
	if(symmetryOn )
		MGlobal::executeCommand("symmetricModelling -e -symmetry false;", false, false);

	if (softSelectionExists) {
		MRichSelection softSelection;
		MGlobal::getRichSelection(softSelection);
		MSelectionList selection, symetry;
		softSelection.getSelection(selection);
		softSelection.getSymmetry(symetry);
		MDagPath dagPath;
		MObject oComp, oCompSymetry;
		for (unsigned int i = 0; i < selection.length(); i++) {
			selection.getDagPath(i, dagPath, oComp);
			symetry.getDagPath(i, dagPath, oCompSymetry);
			if (!(pMesh->dagPath == dagPath)) continue;
			MFnSingleIndexedComponent fnComp(oComp), fnCompSymetry(oCompSymetry);
			for (int i = 0; i < fnComp.elementCount(); i++) {
				vtxWeights[fnComp.element(i)] = fnComp.weight(i).influence();
			}
			for (int i = 0; i < fnCompSymetry.elementCount(); i++) {
				vtxWeights[fnCompSymetry.element(i)] = fnCompSymetry.weight(i).influence();
			}
		}
	}
	else {
		MIntArray vtxIndicesMap = getSelVtxIndicesMap();

		for (unsigned int i = 0; i < vtxIndicesMap.length(); i++) {
			if (vtxIndicesMap[i] == 0)continue;
			vtxWeights[i] = (float)vtxIndicesMap[i];
		}
	}
	if (symmetryOn)
		MGlobal::executeCommand("symmetricModelling -e -symmetry true;", false, false);

	return vtxWeights;
}
