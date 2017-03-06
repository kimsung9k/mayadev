#include "precompile.h"

#include "SGMesh.h"
#include <maya/MFnMesh.h>
#include <maya/MItSelectionList.h>
#include <maya/MSelectionList.h>
#include <maya/MMeshIntersector.h>
#include <maya/MPointArray.h>
#include <maya/MBoundingBox.h>
#include <maya/MFnSingleIndexedComponent.h>
#include "SGSelection.h"
#include "SGSymmetry.h"
#include "SGMatrix.h"
#include "SGIntersectResult.h"
#include "SGPrintf.h"


SGMesh* SGMesh::pMesh = NULL;

SGMesh::SGMesh() {
	intersector = new MMeshIntersector();
}


SGMesh::SGMesh(MDagPath dagPath, const SGSymmetry symInfo)
{
	intersector = new MMeshIntersector();
	this->setDagPath(dagPath, symInfo);
}


SGMesh::~SGMesh() {
	delete intersector;
}



bool SGMesh::update( const SGSymmetry& symInfo, bool force ) {
	MFnMesh fnMesh = dagPath;
	if (!force && !updateRequired()) return true;

	numVertices = fnMesh.numVertices();
	numEdges = fnMesh.numEdges();
	numPolygons = fnMesh.numPolygons();

	if (!updateVertexAndNormals()) return false;
	if (!updateBaseMesh()) return false;
	if (!updateMirror( symInfo )) return false;
	return true;
}



bool SGMesh::updateVertexAndNormals()
{
	MFnMesh fnMesh = dagPath;
	fnMesh.getPoints(points);
	fnMesh.getVertexNormals(true, normals);
	return true;
}



bool SGMesh::updateBaseMesh()
{
	MFnMesh fnMesh(dagPath);
	MFnMesh fnMeshBase(oSlidingBaseMesh);
	if (fnMesh.numVertices() != fnMeshBase.numVertices() ||
		fnMesh.numEdges() != fnMeshBase.numEdges() ||
		fnMesh.numPolygons() != fnMeshBase.numPolygons()) {
		MFnMeshData meshData;
		oSlidingBaseMesh = meshData.create();
		fnMesh.copy(dagPath.node(), oSlidingBaseMesh);
	}
	else {
		fnMeshBase.setPoints(points);
	}
	return true;
}



bool SGMesh::updateMirror(const SGSymmetry& symInfo) {
	mirrorIndices.setLength(points.length());
	for (unsigned int i = 0; i < mirrorIndices.length(); i++)
		mirrorIndices[i] = -1;

	MPointOnMesh pointOnMesh;
	delete intersector;
	intersector = new MMeshIntersector();
	intersector->create(oSlidingBaseMesh);

	for (unsigned int i = 0; i < points.length(); i++) {
		if (mirrorIndices[i] != -1) continue;
		MPoint mirrorPoint = symInfo.convertPointByMirror(points[i]);
		intersector->getClosestPoint(mirrorPoint, pointOnMesh);
		MIntArray vtxList = getPolyToVtxs(pointOnMesh.faceIndex());
		double closeDist = 1000000.0;
		int closeIndex = vtxList[0];
		for (unsigned int j = 0; j < vtxList.length(); j++) {
			double dist = points[vtxList[j]].distanceTo(mirrorPoint);
			if (dist < closeDist) {
				closeDist = dist;
				closeIndex = vtxList[j];
			}
		}
		mirrorIndices[i] = closeIndex;
	}
	return true;
}


MStatus SGMesh::getSelection(const SGSymmetry symInfo)
{
	if (SGMesh::pMesh != NULL) delete SGMesh::pMesh;

	SGMesh::pMesh = new SGMesh();

	MStatus status;
	SGMesh::pMesh->dagPath = MDagPath();
	MSelectionList selectionList;
	MGlobal::getActiveSelectionList(selectionList);
	if (!selectionList.length()) return MS::kFailure;

	MItSelectionList itList(selectionList);
	MDagPath pathNode;
	unsigned int numShapes;

	bool pathExists = false;
	for (; !itList.isDone(); itList.next())
	{
		status = itList.getDagPath(pathNode);
		if (pathNode.node().hasFn(MFn::kMesh))
		{
			MFnDagNode fnDag(pathNode);
			if (!fnDag.isIntermediateObject())
			{
				pMesh->dagPath = pathNode;
				pathExists = true;
			}
		}
		if (pathExists) break;
		CHECK_MSTATUS_AND_RETURN_IT(status);
		numShapes = pathNode.childCount();
		for (unsigned int i = 0; i < numShapes; ++i)
		{
			status = pathNode.push(pathNode.child(i));
			CHECK_MSTATUS_AND_RETURN_IT(status);

			if (pathNode.node().hasFn(MFn::kMesh))
			{
				MFnDagNode fnDag(pathNode);
				if (!fnDag.isIntermediateObject())
				{
					pMesh->dagPath = pathNode;
					pathExists = true;
					break;
				}
			}
			pathNode.pop();
		}
		if (pathExists) break;
	}

	if (!pathExists) return MS::kFailure;
	pMesh->setDagPath( pMesh->dagPath, symInfo );

	return MS::kSuccess;
}


void SGMesh::setDagPath(MDagPath dagPath, const SGSymmetry symInfo )
{
	this->dagPath = dagPath;
	update(symInfo, true );
}


MIntArray SGMesh::getVtxToVtxs(int indexVtx)  const {
	MItMeshVertex itVertex(dagPath);
	int prevIndex;
	itVertex.setIndex(indexVtx, prevIndex);
	MIntArray resultIndices;
	itVertex.getConnectedVertices(resultIndices);
	return resultIndices;
}


MIntArray SGMesh::getVtxToEdges(int indexVtx)  const {
	MItMeshVertex itVertex(dagPath);
	int prevIndex;
	itVertex.setIndex(indexVtx, prevIndex);
	MIntArray resultIndices;
	itVertex.getConnectedEdges(resultIndices);
	return resultIndices;
}


MIntArray SGMesh::getVtxToPolys(int indexVtx)  const {
	MItMeshVertex itVertex(dagPath);
	int prevIndex;
	itVertex.setIndex(indexVtx, prevIndex);
	MIntArray resultIndices;
	itVertex.getConnectedFaces(resultIndices);
	return resultIndices;
}

 
MIntArray SGMesh::getEdgeToVtxs(int indexEdge)  const {
	int2 vtxList;
	MFnMesh fnMesh(dagPath);
	fnMesh.getEdgeVertices(indexEdge, vtxList);
	MIntArray resultIndices;
	resultIndices.setLength(2);
	resultIndices[0] = vtxList[0];
	resultIndices[1] = vtxList[1];
	return resultIndices;
}


MIntArray SGMesh::getEdgeToEdges(int indexEdge)  const {
	MItMeshEdge itEdge(dagPath);
	int prevIndex;
	itEdge.setIndex(indexEdge, prevIndex);
	MIntArray resultIndices;
	itEdge.getConnectedEdges(resultIndices);
	return resultIndices;
}


MIntArray SGMesh::getEdgeToPolys(int indexEdge)  const {
	MItMeshEdge itEdge(dagPath);
	int prevIndex;
	itEdge.setIndex(indexEdge, prevIndex);
	MIntArray resultIndices;
	itEdge.getConnectedFaces(resultIndices);
	return resultIndices;
}


MIntArray SGMesh::getPolyToVtxs(int indexPoly)  const {
	MItMeshPolygon itPolygon(dagPath);
	int prevIndex;
	itPolygon.setIndex(indexPoly, prevIndex);
	MIntArray resultIndices;
	itPolygon.getVertices(resultIndices);
	return resultIndices;
}



MIntArray SGMesh::getPolyToEdges(int indexPoly)  const {
	MItMeshPolygon itPolygon(dagPath);
	int prevIndex;
	itPolygon.setIndex(indexPoly, prevIndex);
	MIntArray resultIndices;
	itPolygon.getEdges(resultIndices);
	return resultIndices;
}


MIntArray SGMesh::getPolyToPolys(int indexPoly)  const {
	MItMeshPolygon itPolygon(dagPath);
	int prevIndex;
	itPolygon.setIndex(indexPoly, prevIndex);
	MIntArray resultIndices;
	itPolygon.getConnectedFaces(resultIndices);
	return resultIndices;
}



bool SGMesh::isCenter(int index, SGComponentType compType ) const {
	if (compType == SGComponentType::kVertex) {
		if (mirrorIndices[index] == index) return true;
	}
	if (compType == SGComponentType::kEdge) {
		MIntArray vtxList = getEdgeToVtxs(index);
		if (isCenter(vtxList[0], SGComponentType::kVertex) &&
			isCenter(vtxList[1], SGComponentType::kVertex)) {
			return true;
		}
	}
	if (compType == SGComponentType::kPolygon) {
		MIntArray vtxList = getEdgeToVtxs(index);
		for (unsigned int i = 0; i < vtxList.length(); i++) {
			if (isCenter(vtxList[i], SGComponentType::kVertex)) continue;
			int mirrorIndex = mirrorIndices[vtxList[i]];
			for (unsigned int j = 0; j < vtxList.length(); j++) {
				if (vtxList[j] == mirrorIndex) return true;
			}
		}
	}
	return false;
}



bool SGMesh::isTwoEdgeHasRelation(int index1, int index2) const {
	MIntArray edges = getEdgeToEdges(index1);
	for (unsigned int i = 0; i < edges.length(); i++) {
		if (edges[i] == index2) return true;
	}
	return false;
}



bool SGMesh::isTwoSplitPointsHasRelation(
	const SGSplitPoint& spPoint1,
	const SGSplitPoint& spPoint2, int* indexPolygon )const
{
	if (spPoint1.dagPath == spPoint2.dagPath) {}
	else return false;

	MIntArray compairPolys1, compairPolys2;
	if (spPoint1.typ == SGComponentType::kVertex)
		compairPolys1 = getVtxToPolys(spPoint1.index);
	else if (spPoint1.typ == SGComponentType::kEdge)
		compairPolys1 = getEdgeToPolys(spPoint1.index);
	else if (spPoint1.typ == SGComponentType::kPolygon)
		compairPolys1 = spPoint1.index;

	if (spPoint2.typ == SGComponentType::kVertex)
		compairPolys2 = getVtxToPolys(spPoint2.index);
	else if (spPoint2.typ == SGComponentType::kEdge)
		compairPolys2 = getEdgeToPolys(spPoint2.index);
	else if (spPoint2.typ == SGComponentType::kPolygon)
		compairPolys2 = spPoint2.index;

	for ( unsigned int i = 0; i < compairPolys1.length(); i++) {
		for (unsigned int j = 0; j < compairPolys2.length(); j++) {
			if (compairPolys1[i] == compairPolys2[j]) {
				if(indexPolygon!=NULL)
				*indexPolygon = compairPolys1[i];
				return true;
			}
		}
	}
	return false;
}


bool SGMesh::isTwoSplitPointsHasSameEdge(const SGSplitPoint& spPoint1, const SGSplitPoint& spPoint2)const
{
	if (spPoint1.dagPath == spPoint2.dagPath) {}
	else return false;

	MIntArray edges1, edges2;
	if (spPoint1.typ == SGComponentType::kVertex) {
		edges1 = getVtxToEdges(spPoint1.index);
	}
	else if (spPoint1.typ == SGComponentType::kEdge) {
		if (spPoint1.param == 1)
		{
			MFnMesh fnMesh(dagPath);
			int2 vtxList;
			fnMesh.getEdgeVertices(spPoint1.index%fnMesh.numEdges(), vtxList);
			edges1 = getVtxToEdges(vtxList[1]);
		}
		else
			edges1.append(spPoint1.index);
	}

	if (spPoint2.typ == SGComponentType::kVertex) {
		edges2 = getVtxToEdges(spPoint2.index);
	}
	else if (spPoint2.typ == SGComponentType::kEdge) {
		if (spPoint2.param == 1)
		{
			MFnMesh fnMesh(dagPath);
			int2 vtxList;
			fnMesh.getEdgeVertices(spPoint2.index%fnMesh.numEdges(), vtxList);
			edges2 = getVtxToEdges(vtxList[1]);
		}
		else
			edges2.append(spPoint2.index);
	}

	for (unsigned int i = 0; i < edges1.length(); i++) {
		for (unsigned int j = 0; j < edges2.length(); j++) {
			if (edges1[i] == edges2[j]) return true;
		}
	}
	return false;
}


bool SGMesh::isTwoVertexHasSameEdge(int index1, int index2) const {
	MIntArray edges1 = getVtxToEdges(index1);
	MIntArray edges2 = getVtxToEdges(index2);

	for (unsigned int i = 0; i < edges1.length(); i++) {
		for (unsigned int j = 0; j < edges2.length(); j++) {
			if (edges1[i] == edges2[j]) return true;
		}
	}
	return false;
}


void SGMesh::getSplitEdgeAndParam(const SGSplitPoint& spPoint, 
	int& edge, float& param, int indexPolygon) const {
	if (spPoint.typ == SGComponentType::kVertex) {
		MIntArray polyToEdges;
		if( indexPolygon != -1 )
			polyToEdges = getPolyToEdges(indexPolygon);
		MIntArray vtxToEdges = getVtxToEdges(spPoint.index);
		int indexEdge = -1;
		for (unsigned int i = 0; i < polyToEdges.length(); i++) {
			for (unsigned int j = 0; j < vtxToEdges.length(); j++) {
				if (polyToEdges[i] == vtxToEdges[j])
					indexEdge = polyToEdges[i];
			}
		}
		if (indexEdge == -1)
			edge = vtxToEdges[0];
		else
			edge = indexEdge;

		MFnMesh fnMesh(dagPath);
		int2 vtxList;
		fnMesh.getEdgeVertices(edge, vtxList);
		if (vtxList[0] == spPoint.index)
			param = 0.0f;
		else
			param = 1.0f;
	}
	else if (spPoint.typ == SGComponentType::kEdge) {
		edge  = spPoint.index;
		param = spPoint.param;
	}
}



bool SGMesh::getSplitEdgesAndParams(
	const SGSplitPoint& spPoint1, const SGSplitPoint& spPoint2,
	MIntArray& edges, MFloatArray& params )const
{
	edges.setLength(2);
	params.setLength(2);

	int indexPolygon = -1;
	isTwoSplitPointsHasRelation(spPoint1, spPoint2, &indexPolygon);

	getSplitEdgeAndParam(spPoint1, edges[0], params[0], indexPolygon);
	getSplitEdgeAndParam(spPoint2, edges[1], params[1], indexPolygon);
	return true;
}



MPoint SGMesh::getPoint(int indexVtx, MSpace::Space space) const {
	MFnMesh fnMesh = dagPath;
	MPoint point;
	fnMesh.getPoint(indexVtx, point, space);
	return point;
}


MPoint SGMesh::getEdgeCenter(int indexEdge, MSpace::Space space) const {
	MPointArray points = getEdgePoints(indexEdge, space);
	return (points[0] + points[1]) / 2;
}



MIntArray SGMesh::getEdgeOpositIndices(int indexEdge, int otherOposit)const
{
	MIntArray returnTargets;

	MIntArray& connectedEdges = getEdgeToEdges(indexEdge);
	MIntArray& connectedFaces = getEdgeToPolys(indexEdge);

	for (unsigned int i = 0; i < connectedFaces.length(); i++) {
		MIntArray& edges = getPolyToEdges(connectedFaces[i]);
		if (edges.length() != 4) continue;
		for (unsigned int j = 0; j < edges.length(); j++) {
			int compairIndex = edges[j];
			if (compairIndex == indexEdge) continue;
			bool sameExists = false;
			for (unsigned int k = 0; k < connectedEdges.length(); k++) {
				if (compairIndex == connectedEdges[k]) {
					sameExists = true;
					break;
				}
			}
			if (sameExists)continue;
			if (otherOposit != -1 && compairIndex == otherOposit) continue;
			returnTargets.append(compairIndex);
		}
	}
	return returnTargets;
}


bool hasSameIndex(const MIntArray& indices1, const MIntArray& indices2) {
	for (unsigned int i = 0; i < indices1.length(); i++) {
		for (unsigned int j = 0; j < indices2.length(); j++) {
			if (indices1[i] == indices2[j])
				return true;
		}
	}
	return false;
}


MIntArray SGMesh::getEdgeSideIndices(int indexEdge, int otherSide) const
{
	MIntArray returnTargets;

	int compairLength = 4;
	MIntArray& polys = getEdgeToPolys(indexEdge);
	if (polys.length() == 1) compairLength = 3;

	MIntArray otherSideList;

	MIntArray& indicesVtxs = getEdgeToVtxs(indexEdge);
	MIntArray& indicesPolys = getEdgeToPolys(indexEdge);

	for (unsigned int j = 0; j < indicesVtxs.length(); j++) {
		MIntArray& vtxToEdges = getVtxToEdges(indicesVtxs[j]);
		if (vtxToEdges.length() != compairLength) continue;
		for (unsigned int k = 0; k < vtxToEdges.length(); k++) {
			if (vtxToEdges[k] == indexEdge || 
				vtxToEdges[k] == otherSide) continue;
			MIntArray& polys = getEdgeToPolys(vtxToEdges[k]);
			if (hasSameIndex(polys, indicesPolys)) continue;
			returnTargets.append(vtxToEdges[k]);
		}
	}

	return returnTargets;
}



MIntArray SGMesh::getEdgeRing(int indexEdge, int beforeIndex)const
{
	MIntArray ringEdges;

	MIntArray indices;
	MIntArray opasitIndices = getEdgeOpositIndices(indexEdge);

	bool lineContinued = false;

	for (unsigned int i = 0; i < opasitIndices.length(); i++)
	{
		int rootEdge = indexEdge;
		int targetEdge = opasitIndices[i];
		int loopLength = 0;
		if (i == 0)ringEdges.append(rootEdge);
		while (true)
		{
			if (i == 0) ringEdges.append(targetEdge);
			else ringEdges.insert(targetEdge, 0);
			MIntArray localOpasitIndices = getEdgeOpositIndices(targetEdge, rootEdge);
			if (!localOpasitIndices.length()) break;
			if (indexEdge == localOpasitIndices[0]) {
				lineContinued = true;
				break;
			}
			rootEdge = targetEdge;
			targetEdge = localOpasitIndices[0];
		}
		if (lineContinued) break;
	}

	

	if (beforeIndex != -1) {
		bool oppositeExists = false;
		for (unsigned int i = 0; i < opasitIndices.length(); i++) {
			if (opasitIndices[i] == beforeIndex) {
				oppositeExists = true;
				break;
			}
		}
		if (oppositeExists) return ringEdges;

		MIntArray startAndEnd;
		MIntArray newEdges;
		MIntArray oppositeEdges;
		for (unsigned int i = 0; i < ringEdges.length(); i++) {
			if (ringEdges[i] == indexEdge || ringEdges[i] == beforeIndex) {
				startAndEnd.append(i);
			}
		}
		if ( startAndEnd.length() != 2) return MIntArray();
		newEdges.setLength(startAndEnd[1] - startAndEnd[0] + 1);
		for (unsigned int i = 0; i < newEdges.length(); i++) {
			newEdges[i] = ringEdges[i + startAndEnd[0]];
		}
		if (lineContinued) {
			oppositeEdges.setLength(ringEdges.length() - newEdges.length() + 2);
			for (unsigned int i = 0; i < oppositeEdges.length(); i++) {
				int oppositeIndex = (startAndEnd[1] + i) % ringEdges.length();
				oppositeEdges[i] = ringEdges[oppositeIndex];
			}
			if (oppositeEdges.length() > newEdges.length()) return newEdges;
			return oppositeEdges;
		}
		return newEdges;
	}

	return ringEdges;
}



MIntArray SGMesh::getEdgeLoop(int indexEdge, int beforeIndex )const
{
	MIntArray loopEdges;
	MIntArray sideEdges = getEdgeSideIndices(indexEdge);
	loopEdges.append(indexEdge);

	bool lineContinued = false;
	for (unsigned int i = 0; i < sideEdges.length(); i++) {
		int rootEdge = indexEdge;
		int targetEdge = sideEdges[i];
		while (true) {
			if (targetEdge == indexEdge) break;
			if (i == 0)loopEdges.append(targetEdge);
			else loopEdges.insert(targetEdge, 0);
			MIntArray localSideEdges = getEdgeSideIndices(targetEdge, rootEdge);
			if (!localSideEdges.length()) break;
			rootEdge = targetEdge;
			targetEdge = localSideEdges[0];
		}
		if (targetEdge == indexEdge) {
			lineContinued = true;
			break;
		}
	}

	for (unsigned int i = 0; i < sideEdges.length(); i++) {
		if (sideEdges[i] == beforeIndex) {
			return loopEdges;
		}
	}

	if (beforeIndex != -1) {
		MIntArray startAndEnd;
		MIntArray newEdges;
		MIntArray oppositeEdges;
		for (unsigned int i = 0; i < loopEdges.length(); i++) {
			if (loopEdges[i] == indexEdge || loopEdges[i] == beforeIndex) {
				startAndEnd.append(i);
			}
		}
		if (startAndEnd.length() != 2) return loopEdges;
		newEdges.setLength(startAndEnd[1] - startAndEnd[0] + 1);
		for (unsigned int i = 0; i < newEdges.length(); i++) {
			newEdges[i] = loopEdges[i + startAndEnd[0]];
		}
		if (lineContinued) {
			oppositeEdges.setLength(loopEdges.length() - newEdges.length() + 2);
			for (unsigned int i = 0; i < oppositeEdges.length(); i++) {
				int oppositeIndex = (startAndEnd[1] + i) % loopEdges.length();
				oppositeEdges[i] = loopEdges[oppositeIndex];
			}
			if (oppositeEdges.length() > newEdges.length()) return newEdges;
			return oppositeEdges;
		}
		return newEdges;
	}

	return loopEdges;
}


MIntArray SGMesh::getVertexLoop(int indexVtx, int beforeIndex )const
{
	MIntArray resultIndices;
	if (indexVtx == beforeIndex) return resultIndices;

	MIntArray edgeIndices = getVtxToEdges(indexVtx);
	int edgeIndex = -1;
	for (unsigned int i = 0; i < edgeIndices.length(); i++) {
		MIntArray vtxIndices = getEdgeToVtxs(edgeIndices[i]);
		if (vtxIndices[0] == beforeIndex || vtxIndices[1] == beforeIndex)
			edgeIndex = edgeIndices[i];
	}
	if (edgeIndex != -1) {
		MIntArray indicesEdges = getEdgeLoop(edgeIndex);
		resultIndices = convertComponent(indicesEdges, SGComponentType::kEdge, SGComponentType::kVertex);
	}
	else {
		MIntArray edgeLoopIndices;
		MIntArray vtxLoopIndices;
		bool loopVtxExists = false;
		for (unsigned int i = 0; i < edgeIndices.length(); i++) {
			edgeLoopIndices = getEdgeLoop(edgeIndices[i]);
			vtxLoopIndices = convertComponent(edgeLoopIndices, SGComponentType::kEdge, SGComponentType::kVertex);
			for (unsigned int j = 0; j < vtxLoopIndices.length(); j++) {
				if (vtxLoopIndices[j] == beforeIndex) {
					loopVtxExists = true; break;
				}
			}
			if (loopVtxExists) break;
			
		}
		if (loopVtxExists) {
			MIntArray firstEdgeIndices;
			MIntArray firstEdgeMap = getVtxToEdges(indexVtx);
			MIntArray beforeEdgeIndices;
			MIntArray beforeEdgeMap = getVtxToEdges(beforeIndex);

			for (unsigned int i = 0; i < firstEdgeMap.length(); i++) {
				for (unsigned int j = 0; j < beforeEdgeMap.length(); j++) {
					if (isTwoEdgeHasRelation(firstEdgeMap[i], beforeEdgeMap[j])) {
						MIntArray edges; edges.setLength(2);
						edges[0] = firstEdgeMap[i];
						edges[1] = beforeEdgeMap[j];
						return convertComponent(edges, SGComponentType::kEdge, SGComponentType::kVertex);
					}
				}
			}
			
			for (unsigned int i = 0; i < edgeLoopIndices.length(); i++) {
				for (unsigned int j = 0; j < firstEdgeMap.length(); j++) {
					if (firstEdgeMap[j] == edgeLoopIndices[i]) firstEdgeIndices.append(firstEdgeMap[j]);
				}
				for (unsigned int j = 0; j < beforeEdgeMap.length(); j++) {
					if (beforeEdgeMap[j] == edgeLoopIndices[i]) beforeEdgeIndices.append(beforeEdgeMap[j]);
				}
			}

			MIntArray shortLengthIndices;
			int shortLength = 10000000;
			for (unsigned int i = 0; i < firstEdgeIndices.length(); i++) {
				for (unsigned int j = 0; j < beforeEdgeIndices.length(); j++) {
					MIntArray edgeLoopIndices = getEdgeLoop(firstEdgeIndices[i], beforeEdgeIndices[j]);
					if ( edgeLoopIndices.length() < (unsigned int)shortLength ) {
						shortLength = edgeLoopIndices.length();
						shortLengthIndices = edgeLoopIndices;
					}
				}
			}
			return convertComponent(shortLengthIndices, SGComponentType::kEdge, SGComponentType::kVertex);
		}
	}
	return resultIndices;
}


MIntArray SGMesh::getPolygonLoop( int indexPoly, int beforeIndex )const
{
	MIntArray edges1 = getPolyToEdges(indexPoly);
	MIntArray edges2 = getPolyToEdges(beforeIndex);
	int sameEdge = -1;
	for (unsigned int i = 0; i < edges1.length(); i++) {
		for (unsigned int j = 0; j < edges2.length(); j++) {
			if (edges1[i] == edges2[j]) { sameEdge = edges1[i]; break; }
		}
	}
	if (sameEdge != -1) {
		MIntArray ringEdges = getEdgeRing(sameEdge);
		MIntArray indicesPolygons = convertComponent(ringEdges, SGComponentType::kEdge, SGComponentType::kPolygon);
		return indicesPolygons;
	}

	MIntArray returnIndices;
	MIntArray ringEdges;
	bool exist = false;

	for (unsigned int i = 0; i < edges1.length(); i++) {
		ringEdges = getEdgeRing(edges1[i]);
		if (hasSameIndex(ringEdges, edges2)) {
			exist = true; break;
		}
	}

	if (!exist) return returnIndices;

	MIntArray existsIndicesFirst;
	MIntArray existsIndicesSecond;

	for (unsigned int i = 0; i < ringEdges.length(); i++) {
		for (unsigned int j = 0; j < edges1.length(); j++) {
			if (edges1[j] == ringEdges[i]) {
				existsIndicesFirst.append(edges1[j]);
			}
		}
		for (unsigned int j = 0; j < edges2.length(); j++) {
			if (edges2[j] == ringEdges[i]) {
				existsIndicesSecond.append(edges2[j]);
			}
		}
	}

	MIntArray ringEdgesLong;
	for (unsigned int i = 0; i < existsIndicesFirst.length(); i++) {
		for (unsigned int j = 0; j < existsIndicesSecond.length(); j++) {
			int indexPolygon = getPolygonFromTwoEdge(existsIndicesFirst[i], existsIndicesSecond[j]);
			if (indexPolygon != -1) continue;
			MIntArray ringEdgesTemp = getEdgeRing(existsIndicesFirst[i], existsIndicesSecond[j]);
			if (ringEdgesTemp.length() > ringEdgesLong.length()) {
				ringEdgesLong = ringEdgesTemp;
			}
		}
	}

	if (!ringEdgesLong.length()) return MIntArray();

	returnIndices.setLength(ringEdgesLong.length() - 1);
	for (unsigned int i = 0; i < returnIndices.length(); i++) {
		int polygonIndex = getPolygonFromTwoEdge(ringEdgesLong[i], ringEdgesLong[i + 1]);
		if (polygonIndex == -1) {
			returnIndices.setLength(0);
			break;
		}
		returnIndices[i] = polygonIndex;
	}

	return returnIndices;
}


int SGMesh::getPolygonFromTwoEdge(int edgeIndex1, int edgeIndex2) const {
	MIntArray polyIndices1 = getEdgeToPolys(edgeIndex1);
	MIntArray polyIndices2 = getEdgeToPolys(edgeIndex2);

	int returnIndex = -1;
	for (unsigned int i = 0; i < polyIndices1.length(); i++) {
		for (unsigned int j = 0; j < polyIndices2.length(); j++) {
			if (polyIndices1[i] == polyIndices2[j]) {
				returnIndex = polyIndices1[i];
				break;
			}
		}
		if (returnIndex != -1) break;
	}
	return returnIndex;
}







MIntArray SGMesh::convertComponent(MIntArray compIndices, SGComponentType typeSrc, SGComponentType typeDest )const
{
	MIntArray componentMap;
	int length;
	if (typeDest == SGComponentType::kVertex) length = numVertices;
	if (typeDest == SGComponentType::kEdge) length = numEdges;
	if (typeDest == SGComponentType::kPolygon) length = numPolygons;
	componentMap.setLength(numEdges);
	for (unsigned int i = 0; i < componentMap.length(); i++)
		componentMap[i] = 0;

	for (unsigned int i = 0; i < compIndices.length(); i++) {
		MIntArray pConvertMap;
		if (typeSrc == SGComponentType::kEdge && typeDest == SGComponentType::kVertex)
			pConvertMap = getEdgeToVtxs(compIndices[i]);
		else if (typeSrc == SGComponentType::kEdge && typeDest == SGComponentType::kPolygon)
			pConvertMap = getEdgeToPolys(compIndices[i]);
		else if (typeSrc == SGComponentType::kPolygon && typeDest == SGComponentType::kEdge )
			pConvertMap = getPolyToEdges(compIndices[i]);
		else if (typeSrc == SGComponentType::kPolygon && typeDest == SGComponentType::kVertex)
			pConvertMap = getPolyToVtxs(compIndices[i]);

		for (unsigned int j = 0; j < pConvertMap.length(); j++) {
			componentMap[pConvertMap[j]] = 1;
		}
	}

	int trueLength = 0;
	for (unsigned int i = 0; i < componentMap.length(); i++) {
		if (componentMap[i]) trueLength += 1;
	}

	MIntArray results;
	results.setLength(trueLength);

	int cuIndex = 0;
	for (unsigned int i = 0; i < componentMap.length(); i++) {
		if (componentMap[i])
		{
			results[cuIndex] = i;
			cuIndex++;
		}
	}
	return results;
}



MIntArray& SGMesh::getVtxsMap(const SGSplitPoint& spPoint) const {
	if (spPoint.typ == SGComponentType::kVertex) {
		return getVtxToVtxs(spPoint.index);
	}
	return getEdgeToVtxs(spPoint.index);
}

MIntArray& SGMesh::getEdgesMap(const SGSplitPoint& spPoint) const {
	if (spPoint.typ == SGComponentType::kVertex) {
		return getVtxToEdges(spPoint.index);
	}
	return getEdgeToEdges(spPoint.index);
}

MIntArray& SGMesh::getPolysMap(const SGSplitPoint& spPoint) const {
	if (spPoint.typ == SGComponentType::kVertex) {
		return getVtxToPolys(spPoint.index);
	}
	return getEdgeToPolys(spPoint.index);
}


bool SGMesh::updateRequired() {
	MFnMesh fnMesh = dagPath;
	if (numVertices != fnMesh.numVertices() ||
		numEdges != fnMesh.numEdges() ||
		numPolygons != fnMesh.numPolygons()) return true;
	return false;
}






MPointArray SGMesh::getEdgePoints(int edgeIndex, MSpace::Space space) const {
	MFnMesh fnMesh = oSlidingBaseMesh;
	int2 vtxList;
	fnMesh.getEdgeVertices(edgeIndex, vtxList);
	MPointArray points; points.setLength(2);
	fnMesh.getPoint(vtxList[0], points[0]);
	fnMesh.getPoint(vtxList[1], points[1]);
	if (space == MSpace::kWorld) {
		for (unsigned int i = 0; i < points.length(); i++)
			points[i] *= dagPath.inclusiveMatrix();
	}
	return points;
}


MPointArray SGMesh::getPolyPoints(int polyIndex, MSpace::Space space) const {
	MFnMesh fnMesh = dagPath;
	MIntArray vtxList;
	fnMesh.getPolygonVertices(polyIndex, vtxList);
	MPointArray points; points.setLength(vtxList.length());
	for ( unsigned int i = 0; i < points.length(); i++) {
		fnMesh.getPoint(vtxList[i], points[i], space);
	}
	return points;
}


MVector SGMesh::getEdgeVector(int edgeIndex, MSpace::Space space)const
{
	MFnMesh fnMesh = dagPath;
	int2 vtxList;
	fnMesh.getEdgeVertices(edgeIndex, vtxList);
	MPoint point1, point2;
	fnMesh.getPoint(vtxList[0], point1, space);
	fnMesh.getPoint(vtxList[1], point2, space);
	return point2 - point1;
}



MIntArray SGMesh::getInverseDirectionInfo( int rootEdge, const MIntArray& otherIndices)const
{
	MIntArray inverseInfo;
	inverseInfo.setLength(otherIndices.length());

	for (unsigned int i = 0; i < inverseInfo.length(); i++) {
		inverseInfo[i] = 0;
	}

	int rootElementIndex = -1;
	for (unsigned int i = 0; i < otherIndices.length(); i++)
	{
		if (rootEdge == otherIndices[i])
			rootElementIndex = i;
	}

	if (rootElementIndex == -1)
		return inverseInfo;

	MVector rootVector = getEdgeVector(rootEdge);
	for (unsigned int i = rootElementIndex; i < otherIndices.length(); i++)
	{
		MVector edgeVector = getEdgeVector(otherIndices[i]);
		if (edgeVector*rootVector < 0) {
			rootVector = -edgeVector;
			inverseInfo[i] = 1;
		}
		else {
			rootVector = edgeVector;
			inverseInfo[i] = 0;
		}
	}
	rootVector = getEdgeVector(rootEdge);
	for (int i = rootElementIndex; i >= 0; i--)
	{
		MVector edgeVector = getEdgeVector(otherIndices[i]);
		if (edgeVector*rootVector < 0) {
			rootVector = -edgeVector;
			inverseInfo[i] = 1;
		}
		else {
			rootVector = edgeVector;
			inverseInfo[i] = 0;
		}
	}
	return inverseInfo;
}


MPoint SGMesh::getPointFromEdgeParam(int indexEdge, float param, MSpace::Space space)const
{
	MFnMesh fnMesh = dagPath;
	int2 vtxList;
	fnMesh.getEdgeVertices(indexEdge%fnMesh.numEdges(), vtxList);
	MPoint point1, point2;
	fnMesh.getPoint(vtxList[0], point1, space);
	fnMesh.getPoint(vtxList[1], point2, space);
	return (point2 - point1) * (double)param + point1;
}


bool SGMesh::isOppositeEdge(int baseEdge, int targetEdge)const
{
	MIntArray polyIndices = getEdgeToPolys(baseEdge);

	bool isRelativeEdge = false;
	for (int i = 0; i < (int)polyIndices.length(); i++) {
		MIntArray& indicesEdges = getPolyToEdges(polyIndices[i]);
		for (int j = 0; j < (int)indicesEdges.length(); j++)
		{
			if (indicesEdges[j] == targetEdge) {
				isRelativeEdge = true;
				break;
			}
		}
		if (isRelativeEdge) break;
	}
	return isRelativeEdge;
}


MIntArray SGMesh::getIndicesNewEdgeRing(int numNewEdges, bool oppositeExists, int offset ) const
{
	int numEdges = MFnMesh(dagPath).numEdges();
	MIntArray newEdgeIndices;
	newEdgeIndices.setLength(numNewEdges);
	for (int i = 0; i < numNewEdges; i++)
		newEdgeIndices[i] = offset + numEdges + (i + 1) * 2;
	if (oppositeExists) newEdgeIndices.append(offset + numEdges + numNewEdges * 2 + 1);
	return newEdgeIndices;
}


MPoint SGMesh::getPolygonCenter(int indexPoly, MSpace::Space space)const
{
	const MIntArray& vtxIndices = getPolyToVtxs(indexPoly);

	MBoundingBox bb;
	MPoint point;
	for (unsigned int i = 0; i < vtxIndices.length(); i++) {
		bb.expand(points[vtxIndices[i]]);
	}
	return bb.center();
}


MVector SGMesh::getPolygonNormal(int indexPoly, MSpace::Space space)const
{
	MFnMesh fnMesh(dagPath);
	MVector normal(0, 0, 0);
	fnMesh.getPolygonNormal(indexPoly, normal, space);
	return normal;
}



MIntArray SGMesh::getSlideTargetIndices(int indexSlideRoot, int indexSlideOpposite, const MIntArray& indicesSlideMap, MIntArray& checkedMap, int beforeRoot ) const {
	MIntArray targetIndices;
	targetIndices.append(indexSlideOpposite);
	if (checkedMap[indexSlideRoot]) return targetIndices;
	checkedMap[indexSlideRoot] = 1;
	const MIntArray& sideIndicesRoot = getEdgeToEdges(indexSlideRoot);
	const MIntArray& sideIndicesOpposite = getEdgeToEdges(indexSlideOpposite);

	for (unsigned int i = 0; i < sideIndicesRoot.length(); i++) {
		//if (sideIndicesRoot[i] == indexSlideRoot) continue;
		int sideRootIndex = sideIndicesRoot[i];
		int sideOppositeIndex = -1;
		if (beforeRoot == sideRootIndex) continue;
		if (indicesSlideMap[sideRootIndex]) {
			MIntArray oppositeIndices = getEdgeOpositIndices(sideRootIndex);
			for (unsigned int j = 0; j < sideIndicesOpposite.length(); j++) {
				for (unsigned int k = 0; k < oppositeIndices.length(); k++) {
					if (sideIndicesOpposite[j] == oppositeIndices[k]){
						sideOppositeIndex = oppositeIndices[k]; break;
					}
				}
				if (sideOppositeIndex != -1) break;
			}
		}
		if (sideOppositeIndex != -1) {
			MIntArray sideTargetIndices = getSlideTargetIndices(sideRootIndex, sideOppositeIndex, indicesSlideMap, checkedMap, indexSlideRoot);
			for (unsigned int j = 0; j < sideTargetIndices.length(); j++)
				targetIndices.append(sideTargetIndices[j]);
		}
	}
	return targetIndices;
}

MPointArray SGMesh::getIntersectedLinePoints(MPoint lineSrc, MPoint lineDst, const MMatrix& camMatrix, MIntArray* edges, MFloatArray* params) const {

	MPoint viewLineSrc = SGMatrix::getViewPointFromWorld(lineSrc, camMatrix);
	MPoint viewLineDst = SGMatrix::getViewPointFromWorld(lineDst, camMatrix);

	MBoundingBox bbMain;
	bbMain.expand(viewLineSrc);
	bbMain.expand(viewLineDst);

	double minX = bbMain.min().x;
	double minY = bbMain.min().y;
	double maxX = bbMain.max().x;
	double maxY = bbMain.max().y;

	MVector lineVector = viewLineDst - viewLineSrc;

	MDoubleArray lengthList;

	MPointArray resultPoints;
	if (lineVector.length() < 1) return resultPoints;

	MMatrix worldToView = SGMatrix::getWorldToViewMatrix(camMatrix);
	MFnMesh fnMesh = dagPath;

	int numChecked = 0;

	MIntArray edgeIndices;
	MFloatArray edgeParams;

	for (int i = 0; i < numEdges; i++) {
		const MIntArray& polyList = getEdgeToPolys(i);

		const MIntArray& vtxList = getEdgeToVtxs(i);
		MPoint pointSrc = SGMatrix::getViewPointFromWorld(points[vtxList[0]], camMatrix, &worldToView);
		MPoint pointDst = SGMatrix::getViewPointFromWorld(points[vtxList[1]], camMatrix, &worldToView);

		MBoundingBox bbEach;
		bbEach.expand(pointSrc);
		bbEach.expand(pointDst);
		if ((bbEach.min().x < minX && bbEach.min().y < minY) ||
			(bbEach.max().x > maxX && bbEach.max().y > maxY)) {
			continue;
		}

		bool oppositNormal = false;
		for (unsigned int j = 0; j < polyList.length(); j++) {
			MVector polygonNormal = getPolygonNormal( polyList[j] );
			MPoint polyNormalSrc = getPolygonCenter(polyList[j]);
			MPoint polyNormalDst = polyNormalSrc + polygonNormal;
			polyNormalSrc *= worldToView;
			polyNormalDst *= worldToView;
			double value =  polyNormalDst.z / polyNormalDst.w - polyNormalSrc.z / polyNormalSrc.w;
			
			if (value > 0) { oppositNormal = true; break; }
		}
		if (oppositNormal) continue;

		/*
		MPointArray line1; line1.setLength(2);
		MPoint crossPoint = SGMatrix::getCrossPoint(viewLineSrc, viewLineDst, pointSrc, pointDst);
		MPoint viewToWorldPoint = SGMatrix::getWorldPointFromView(crossPoint, camMatrix);
		MVector crossPointVector1 = crossPoint - viewLineSrc;
		if (lineVector * crossPointVector1 < 0) continue;

		MVector pointsVector = pointDst - pointSrc;
		MVector crossPointVector2 = crossPoint - pointSrc;
		if (pointsVector * crossPointVector2 < 0) continue;

		if (crossPointVector1.length() > lineVector.length()) continue;
		if (crossPointVector2.length() > pointsVector.length()) continue;

		lengthList.append( viewLineSrc.distanceTo(crossPoint) );

		SGIntersectResult result = SGIntersectResult::getIntersectionResult((int)crossPoint.x, (int)crossPoint.y, camMatrix);
		edgeIndices.append(result.edgeIndex);
		edgeParams.append(result.edgeParam);
		resultPoints.append(result.intersectPoint);*/
	}
	/*
	MDoubleArray soltedLengthList;
	MIntArray   soltedIndices;
	soltedLengthList.append(lengthList[0]);
	soltedIndices.append(0);
	for (unsigned int i = 1; i < lengthList.length(); i++) {
		bool inserted = false;
		for (unsigned int j = 0; j < soltedLengthList.length(); j++) {
			if (soltedLengthList[j] > lengthList[i]) {
				soltedLengthList.insert(lengthList[i], j);
				soltedIndices.insert(i, j);
				inserted = true;
				break;
			}
		}
		if (!inserted) {
			soltedLengthList.append(lengthList[i]);
			soltedIndices.append(i);
		}
	}

	if (edges != NULL) {
		edges->setLength(edgeIndices.length());
		for (unsigned int i = 0; i < soltedIndices.length(); i++) {
			(*edges)[i] = edgeIndices[soltedIndices[i]];
		}
	}
	if (params != NULL) {
		params->setLength(edgeIndices.length());
		for (unsigned int i = 0; i < soltedIndices.length(); i++) {
			(*params)[i] = edgeParams[soltedIndices[i]];
		}
	}

	MPointArray soltedPoints;
	soltedPoints.setLength(edgeIndices.length());
	for (unsigned int i = 0; i < soltedIndices.length(); i++) {
		soltedPoints[i] = resultPoints[soltedIndices[i]];
	}
	*/
	return MPointArray();
}