#include "precompile.h"
#include "SGGeneralManip.h"
#include "SGTransformManip.h"
#include "SGMouse.h"
#include <SGIntersectResult.h>
#include <SGMatrix.h>
#include <SGMesh.h>
#include <SGSelection.h>
#include <SGSpace.h>
#include <SGSplitPoint.h>
#include "SGColor.h"
#include <SGPrintf.h>


extern SGManip* manip;
extern vector<SGIntersectResult> generalResult;
extern vector<SGIntersectResult> edgeSplitIntersectResult;

extern vector<vector<SGSplitPoint>> spPointsArr;

void SGGeneralManip::build(const MMatrix& camMatrix) {
	this->camMatrix = camMatrix;
}


void SGGeneralManip::drawMousePoint(int manipIndex) {
	MPoint mousePoint(SGMouse::x, SGMouse::y, 0);

	MMatrix camMatrix = SGMatrix::getCamMatrix();
	MMatrix viewToWorldMatrix = SGMatrix::getViewToWorldMatrix(camMatrix);

	int cpLength = 20;
	MPointArray circlePoints; circlePoints.setLength(cpLength);
	float circleSize = 10.0f;
	float eachRad = 3.14159 / cpLength * 2;
	for (int i = 0; i < cpLength; i++) {
		float x = sin(eachRad * i) * circleSize;
		float y = cos(eachRad * i) * circleSize;
		MVector radVector(x, y);
		circlePoints[i] = SGMatrix::getWorldPointFromView(radVector + mousePoint, camMatrix, &viewToWorldMatrix);
	}

	manip->pushPolygon(manipIndex, circlePoints, MColor(1,1,1));
}


void SGGeneralManip::drawDefault(int index) {
	SGIntersectResult* pResult = &generalResult[manipNum];
	if (pResult->resultType == SGComponentType::kNone) return;

	MMatrix camMatrix = SGMatrix::getCamMatrix();

	if (SGMouse::eventType == SGMouse::kMove)
	{
		if (pResult->isVertex()) {
			if (!pResult->itHasOppositNormal(SGMouse::x, SGMouse::y, camMatrix))
				manip->pushPoint(index, pResult->vtxPoint, SGColor::defaultColor, 4);
			else
				manip->pushPoint(index, pResult->vtxPoint, SGColor::defaultOppositeColor, 4);
		}
		else if (pResult->isEdge()) {
			if (!pResult->itHasOppositNormal(SGMouse::x, SGMouse::y, camMatrix))
				manip->pushLine(index, pResult->edgePoints, SGColor::defaultColor);
			else
				manip->pushLine(index, pResult->edgePoints, SGColor::defaultOppositeColor);
		}
		else if (pResult->isPolygon()) {
			if (!pResult->itHasOppositNormal(SGMouse::x, SGMouse::y, camMatrix))
				manip->pushPolygon(index, pResult->polyPoints, SGColor::defaultColor);
			else
				manip->pushPolygon(index, pResult->polyPoints, SGColor::defaultOppositeColor);
		}
	}
}


MDagPath gBeforeDagPath;
bool SGGeneralManip::getSplitPoint(int resultIndex, int index, MPoint& pointOutput)
{
	if (spPointsArr[resultIndex][index].typ == SGComponentType::kNone) return false;

	SGIntersectResult* pResult = &edgeSplitIntersectResult[resultIndex];
	MFnMesh fnMesh;
	if (pResult->resultType == SGComponentType::kNone) {
		if (gBeforeDagPath.node().isNull())return false;
		fnMesh.setObject(gBeforeDagPath);
	}
	else {
		fnMesh.setObject(SGMesh::pMesh->dagPath);
		gBeforeDagPath = SGMesh::pMesh->dagPath;
	}

	if (spPointsArr[resultIndex][index].typ == SGComponentType::kVertex)
	{
		fnMesh.getPoint(spPointsArr[resultIndex][index].index, pointOutput, MSpace::kWorld);
		return true;
	}
	else if (spPointsArr[resultIndex][index].typ == SGComponentType::kEdge)
	{
		int2 vtxList;
		fnMesh.getEdgeVertices(spPointsArr[resultIndex][index].index, vtxList);

		MPoint point1, point2;
		fnMesh.getPoint(vtxList[0], point1, MSpace::kWorld);
		fnMesh.getPoint(vtxList[1], point2, MSpace::kWorld);

		float param = spPointsArr[resultIndex][index].param;
		pointOutput = point1 *(double)(1.0f - param) + point2 * (double)param;
		return true;
	}
	return false;
}

#include <SGPrintf.h>
void SGGeneralManip::drawSPoints(int index) {

	MPoint mousePoint(SGMouse::x, SGMouse::y, 0);
	MPoint worldPoint = SGMatrix::getWorldPointFromView(mousePoint, SGMatrix::getCamMatrix());
	
	for (int i = 0; i < spPointsArr.size(); i++) {
		SGIntersectResult& intersectResult = edgeSplitIntersectResult[i];
		SGSplitPoint newSplitPoint;
		newSplitPoint.dagPath = SGMesh::pMesh->dagPath;
		newSplitPoint.index = intersectResult.resultIndex;
		newSplitPoint.typ = intersectResult.resultType;
		newSplitPoint.point = intersectResult.intersectPoint;
		newSplitPoint.param = intersectResult.edgeParam;

		if (intersectResult.resultType == SGComponentType::kVertex ||
			intersectResult.resultType == SGComponentType::kEdge)
		manip->pushPoint(index, newSplitPoint.getPoint(), SGColor::splitEgeColor, 3);

		if (!spPointsArr[i].size()) continue;
		manip->pushPoint(index, spPointsArr[i][0].getPoint(), SGColor::splitEgeColor, 3);
		for (int j = 1; j < spPointsArr[i].size(); j++) {
			MPoint point1 = spPointsArr[i][j - 1].getPoint();
			MPoint point2 = spPointsArr[i][j].getPoint();
			manip->pushPoint(index, point2, SGColor::splitEgeColor, 3);
			MPointArray points; points.setLength(2);
			points[0] = point1; points[1] = point2;
			manip->pushLine(index, points, SGColor::splitEgeColor);
		}
		int lastIndex = (int)spPointsArr[i].size() - 1;
		if (intersectResult.resultType == SGComponentType::kNone) continue;
		if (intersectResult.resultType == SGComponentType::kPolygon) continue;

		SGMesh* pMesh = SGMesh::pMesh;
		bool hasRelation = pMesh->isTwoSplitPointsHasRelation(spPointsArr[i][lastIndex], newSplitPoint);
		if (hasRelation) {
			bool hasSameEdge = pMesh->isTwoSplitPointsHasSameEdge(spPointsArr[i][lastIndex], newSplitPoint);
			if (hasSameEdge) continue;
		}
		else continue;

		if (SGSplitPoint::isStartEdge(i, newSplitPoint) && spPointsArr[i].size() > 1) {
			newSplitPoint = spPointsArr[i][0];
		}
		MPointArray line; line.setLength(2);
		line[0] = spPointsArr[i][lastIndex].getPoint();
		line[1] = newSplitPoint.getPoint();
		
		manip->pushLine(index, line, SGColor::splitEgeColor);
	}
}


void SGGeneralManip::drawEdgeParamPoint(int index) {
	
}


struct splitRingInfo {
	MDagPath dagPath;
	int beforeIndex;
	MIntArray beforeRings;
	MIntArray getEdgeRing(SGIntersectResult* pResult) {
		bool requirUpdate = false;
		if (dagPath.node().isNull())
			requirUpdate = true;
		else if (!(dagPath == SGMesh::pMesh->dagPath))
			requirUpdate = true;
		else if (pResult->edgeIndex != beforeIndex) {
			requirUpdate = true;
		}

		if (requirUpdate) {
			SGMesh* pMesh = SGMesh::pMesh;
			if (pMesh == NULL) return MIntArray();
			beforeRings = pMesh->getEdgeRing(pResult->edgeIndex);
		}
		return beforeRings;
	}
};

splitRingInfo ringInfo;
void SGGeneralManip::drawSplitRing(int index)
{
	SGIntersectResult* pResult = &edgeSplitIntersectResult[manipNum];
	if ( pResult->resultType == SGComponentType::kNone) return;
	if (!pResult->isEdge()) return;
	SGMesh* pMesh = SGMesh::pMesh;

	MIntArray edgeRings = ringInfo.getEdgeRing(pResult);
	if (manipNum != 0) {
		bool centerExists = false;
		for (unsigned int i = 0; i < edgeRings.length(); i++) {
			MPointArray points = pMesh->getEdgePoints(edgeRings[i], SGSpace::space);
			if (fabs(points[0].x) < 0.0001 && fabs(points[1].x) < 0.0001) {
				centerExists = true;
				break;
			}
		}
		if (centerExists) return;
	}

	GLushort pattern = 0xf0f0;
	MPointArray edgePoints = getEdgeRingPoints(SGMesh::pMesh->dagPath, pResult->edgeIndex, edgeRings, pResult->edgeParam);
	manip->pushLine(index, edgePoints, SGColor::splitEgeColor, 1, &pattern);
}


MPointArray SGGeneralManip::getEdgeRingPoints(MDagPath dagPath, int indexEdge, const MIntArray& indicesEdge, float paramEdge)
{
	SGMesh* pMesh = SGMesh::pMesh;
	MIntArray reverseIndices = pMesh->getInverseDirectionInfo(indexEdge, indicesEdge);

	MPointArray edgePoints; edgePoints.setLength(indicesEdge.length());
	for (unsigned int i = 0; i < indicesEdge.length(); i++) {
		float param = paramEdge;
		if (reverseIndices[i]) param = 1 - param;
		MPoint point = pMesh->getPointFromEdgeParam(indicesEdge[i], param, SGSpace::space);
		edgePoints[i] = point;
	}
	if (!indicesEdge.length()) return edgePoints;
	if (pMesh->isOppositeEdge(indicesEdge[0], indicesEdge[indicesEdge.length() - 1])) {
		edgePoints.append(edgePoints[0]);
	}
	return edgePoints;
}