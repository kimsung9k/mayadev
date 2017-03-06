#include "precompile.h"
#include "SGBase.h"
#include "SGIntersectResult.h"
#include "SGMesh.h"
#include "SGMatrix.h"
#include "SGPrintf.h"

#include <maya/MSelectionList.h>
#include <maya/MFnSet.h>
#include <maya/MFnSingleIndexedComponent.h>


SGIntersectResult::SGIntersectResult() {
}

void SGIntersectResult::setObject(MObject oMesh)
{
	this->vtxIndex = -1;
	this->vtxDist = 10000000.0;
	this->vtxPoint = MPoint(0, 0, 0);

	this->edgeIndex = -1;
	this->edgeParam = 0;
	this->edgeDist = 100000000.0;
	this->edgePoints.setLength(2);

	this->intersectPoint = MPoint(0, 0, 0);
	this->polyIndex = -1;
	this->polyPoints.setLength(0);

	this->gotType = SGComponentType::kNone;
	this->resultType = SGComponentType::kNone;

	this->oMesh = oMesh;
}


void SGIntersectResult::setMeshMatrix(MDagPath dagPath) {
	this->meshMatrix = dagPath.inclusiveMatrix();
}


void SGIntersectResult::setDagPath(MDagPath dagPath) {
	setObject(dagPath.node());
	setMeshMatrix(dagPath);
}


void SGIntersectResult::clearResult()
{
	this->vtxIndex = -1;
	this->vtxDist = 10000000.0;
	this->vtxPoint = MPoint(0, 0, 0);

	this->edgeIndex = -1;
	this->edgeParam = 0;
	this->edgeDist = 100000000.0;
	this->edgePoints.setLength(2);

	this->intersectPoint = MPoint(0, 0, 0);
	this->polyIndex = -1;
	this->polyPoints.setLength(0);

	this->gotType = SGComponentType::kNone;
	this->resultType = SGComponentType::kNone;
}


SGIntersectResult::~SGIntersectResult() {
	this->edgePoints.setLength(2);
}


MPoint SGIntersectResult::getVtxNormalIntersectPoint( int mouseX, int mouseY)
{
	MMatrix worldToView = SGMatrix::getWorldToViewMatrix(camMatrix);

	MPoint point1 = vtxPoint;
	MVector normal = vtxNormal;
	normal.normalize();
	MPoint point2 = point1 + normal;

	MPoint projPoint1 = SGMatrix::getViewPointFromWorld(point1, camMatrix);
	MPoint projPoint2 = SGMatrix::getViewPointFromWorld(point2, camMatrix);

	MPoint xyPoint(mouseX, mouseY, 0, 1);
	MPoint pointProjected;
	float param;
	SGMatrix::getPointAndVectorDist(projPoint1, projPoint2, xyPoint, &pointProjected, &param, false);

	return MVector(point2 - point1)*(double)param + point1;
}


float SGIntersectResult::updateParameter( int mouseX, int mouseY, MPoint* pPointProjected ) {
	MFnMesh fnMesh = oMesh;
	int2 vtxList;
	fnMesh.getEdgeVertices(this->edgeIndex, vtxList);

	MPoint point1, point2;
	fnMesh.getPoint(vtxList[0], point1);
	fnMesh.getPoint(vtxList[1], point2);

	MPoint viewPoint1 = SGMatrix::getViewPointFromWorld(point1 * meshMatrix, camMatrix);
	MPoint viewPoint2 = SGMatrix::getViewPointFromWorld(point2 * meshMatrix, camMatrix);
	MPoint xyPoint(mouseX, mouseY, 0, 1);

	MPoint pointProjected;
	float param;
	SGMatrix::getPointAndVectorDist(viewPoint1, viewPoint2, xyPoint, &pointProjected, &param);

	if (pPointProjected != NULL) {
		*pPointProjected = MVector(point2 - point1)*(double)param + point1;
	}

	edgeParam = param;
	return param;
}


bool SGIntersectResult::isNone() const
{
	if (resultType.typ == SGComponentType::kNone) return true;
	return false;
}


bool SGIntersectResult::isVertex() const
{
	if (resultType.typ == SGComponentType::kVertex) return true;
	return false;
}


bool SGIntersectResult::isEdge() const
{
	if (resultType.typ == SGComponentType::kEdge) return true;
	return false;
}


bool SGIntersectResult::isPolygon() const
{
	if (resultType.typ == SGComponentType::kPolygon) return true;
	return false;
}



SGIntersectResult SGIntersectResult::getIntersectionResult(int x, int y, const MMatrix& inputCamMatrix )
{
	SGIntersectResult result;

	result.setDagPath(SGMesh::pMesh->dagPath);
	SGBase::getIsolateMap(SGMesh::pMesh->dagPath);

	result.camMatrix = inputCamMatrix;
	bool bResult = result.getInsideIntersectionResult(x, y);
	if (!bResult) {
		result.getOutsideIntersectionResult(x, y);
	}
	return result;
}



bool SGIntersectResult::isResultHasNoProblem() {
	if (oMesh.apiType() != MFn::kMesh) return false;
	MFnMesh fnMesh = oMesh;
	int numVertices = fnMesh.numVertices();
	int numEdges    = fnMesh.numEdges();
	int numPolygons = fnMesh.numPolygons();
	if (numVertices <= vtxIndex) return false;
	if (numEdges <= edgeIndex) return false;
	if (numPolygons <= polyIndex) return false;
	return true;
}

bool SGIntersectResult::itHasOppositNormal(int mouseX, int mouseY, const MMatrix& camMatrix ) {
	if (resultType == SGComponentType::kNone) return true;
	if (!isResultHasNoProblem()) return false;

	MFnMesh fnMesh = oMesh;
	MMatrix worldToViewMatrix = SGMatrix::getWorldToViewMatrix(camMatrix);
	MPoint nearClip, farClip;
	SGMatrix::viewToWorld(mouseX, mouseY, nearClip, farClip, camMatrix);
	MVector ray = farClip - nearClip;
	ray.normalize();

	int targetVtxIndex = vtxIndex;
	int targetEdgeIndex = edgeIndex;
	int targetPolyIndex = polyIndex;
	
	SGMesh* pMesh = SGMesh::pMesh;

	if (resultType == SGComponentType::kVertex) {
		MIntArray polyList = pMesh->getVtxToPolys(targetVtxIndex);
		MVector normal;
		for (unsigned int i = 0; i < polyList.length(); i++) {
			fnMesh.getPolygonNormal(polyList[i], normal);
			if (ray * normal < 0) return false;
		}
		return true;
	}
	else if (resultType == SGComponentType::kEdge) {
		MIntArray polyList = pMesh->getEdgeToPolys(targetEdgeIndex);
		MVector normal;
		for (unsigned int i = 0; i < polyList.length(); i++) {
			fnMesh.getPolygonNormal(polyList[i], normal);
			if (ray * normal < 0) return false;
		}
		return true;
	}
	else if (resultType == SGComponentType::kPolygon) {
		MVector normal;
		fnMesh.getPolygonNormal(targetPolyIndex, normal);
		if (ray * normal < 0) return false;
		return true;
	}
	return false;
}



bool SGIntersectResult::getInsideIntersectionResult(int x, int y )
{
	MStatus status;

	M3dView active3dView = M3dView().active3dView();
	int width = active3dView.portWidth();
	int height = active3dView.portHeight();

	MMatrix worldToViewMtx = meshMatrix * SGMatrix::getWorldToViewMatrix(camMatrix);
	MFnMesh fnMesh = oMesh;
	MPointArray meshPoints;
	fnMesh.getPoints(meshPoints);

	float aspect = (float)width / height;
	float xValue = (((float)x / width) * 2 - 1)*aspect;
	float yValue = ((float)y / height) * 2 - 1;
	MPoint xyPoint(xValue, yValue, 0, 1);

	MPoint nearClip, farClip;
	SGMatrix::viewToWorld(x, y, nearClip, farClip, camMatrix);
	MFloatPoint raySource;
	MFloatPointArray hitPoints;

	nearClip *= meshMatrix.inverse();
	farClip  *= meshMatrix.inverse();

	raySource.setCast(nearClip);
	MVector rayDirection = (farClip - nearClip).normal();

	MIntArray hitFace, hitTriangle;

	float closeDist = 100000000.0;
	int targetIndex = -1;
	MPoint rhitPoint;
	MFloatArray hitRayParam;
	int rhitFace = -1;
	bool intersectionResult = fnMesh.allIntersections(
		raySource, rayDirection, NULL, NULL, false, MSpace::kObject,
		1000.0f, false, NULL, true, hitPoints, &hitRayParam, &hitFace, &hitTriangle, NULL, NULL);
	
	if (!intersectionResult || !hitFace.length() ) return false;
	if (SGBase::isolatePolyMap.length()) {
		for (unsigned int i = 0; hitFace.length(); i++) {
			if (SGBase::isolatePolyMap.length() <= hitFace[i]) return false;
			if (SGBase::isolatePolyMap[hitFace[i]]) {
				rhitFace  = hitFace[i];
				rhitPoint = hitPoints[i];
				break;
			}
		}
		if (rhitFace == -1)return false;
	}
	else {
		rhitFace = hitFace[0];
		rhitPoint = hitPoints[0];
	}

	this->polyIndex = rhitFace;
	this->intersectPoint = rhitPoint * meshMatrix;

	MIntArray vtxIndices;
	fnMesh.getPolygonVertices(this->polyIndex, vtxIndices);
	this->polyPoints.setLength(vtxIndices.length());

	double closeDistVtx = 100000.0;
	int closeIndexVtx = vtxIndices[0];
	MPoint closeVtxPoint;
	for (int i = 0; i < (int)vtxIndices.length(); i++) {
		MPoint& point = meshPoints[vtxIndices[i]];
		MPoint viewPoint = point * worldToViewMtx;
		viewPoint.x *= (aspect / viewPoint.w); viewPoint.y /= viewPoint.w; viewPoint.z = 0; viewPoint.w = 1;
		double dist = viewPoint.distanceTo(xyPoint);
		if (dist < closeDistVtx) {
			closeDistVtx = dist;
			closeIndexVtx = vtxIndices[i];
			closeVtxPoint = point;
		}
		this->polyPoints[i] = point * meshMatrix;
	}
	this->vtxDist = closeDistVtx * height / 2;
	this->vtxIndex = closeIndexVtx;
	this->vtxPoint = closeVtxPoint * meshMatrix;

	MItMeshPolygon itPoly(oMesh);
	MIntArray edgeIndices; int prevIndex;
	itPoly.setIndex(this->polyIndex, prevIndex);
	itPoly.getEdges(edgeIndices);
	this->edgePoints.setLength(2);

	double closeDistEdge = 1000000.0;
	int closeIndexEdge = edgeIndices[0];
	MPointArray closeEdgePoints; closeEdgePoints.setLength(2);
	float closeEdgeParam;
	for (int i = 0; i < (int)edgeIndices.length(); i++) {
		int& indexEdge = edgeIndices[i];
		int2 indicesVtx;
		fnMesh.getEdgeVertices(indexEdge, indicesVtx);
		MPoint point1 = meshPoints[indicesVtx[0]];
		MPoint point2 = meshPoints[indicesVtx[1]];
		MPoint viewPoint1 = point1 * worldToViewMtx;
		MPoint viewPoint2 = point2 * worldToViewMtx;
		viewPoint1.x *= (aspect / viewPoint1.w); viewPoint1.y /= viewPoint1.w; viewPoint1.z = 0; viewPoint1.w = 1;
		viewPoint2.x *= (aspect / viewPoint2.w); viewPoint2.y /= viewPoint2.w; viewPoint2.z = 0; viewPoint2.w = 1;
		MPoint pointProjected;
		float  param;
		double dist = SGMatrix::getPointAndVectorDist(viewPoint1, viewPoint2, xyPoint, &pointProjected, &param);
		if (dist < closeDistEdge) {
			closeDistEdge = dist;
			closeIndexEdge = edgeIndices[i];
			closeEdgePoints[0] = point1;
			closeEdgePoints[1] = point2;
			closeEdgeParam = param;
		}
	}

	this->gotType = SGComponentType::kPolygon;
	this->edgeIndex = closeIndexEdge;
	this->edgeDist = closeDistEdge *height / 2.0;
	this->edgePoints = closeEdgePoints; this->edgePoints[0] *= meshMatrix; this->edgePoints[1] *= meshMatrix;
	this->edgeParam = closeEdgeParam;
	if (this->vtxDist < 10) {
		this->resultType = SGComponentType::kVertex;
		this->resultIndex = this->vtxIndex;
	}
	else if (this->edgeDist < 10) {
		this->resultType = SGComponentType::kEdge;
		this->resultIndex = this->edgeIndex;
	}
	else {
		this->resultType = SGComponentType::kPolygon;
		this->resultIndex = this->polyIndex;
	}
	return true;
}




bool SGIntersectResult::getOutsideIntersectionResult(int x, int y) {
	MFnMesh fnMesh = oMesh;

	M3dView active3dView = M3dView().active3dView();
	int width = active3dView.portWidth();
	int height = active3dView.portHeight();

	MMatrix worldToViewMtx = SGMatrix::getWorldToViewMatrix(camMatrix);

	float aspect = (float)width / height;
	float xValue = (((float)x / width) * 2 - 1)*aspect;
	float yValue = ((float)y / height) * 2 - 1;
	float boundX = 10 / (float)height * 2;
	float boundY = 10 / (float)height * 2;
	float boundMinX = xValue - boundX;
	float boundMaxX = xValue + boundX;
	float boundMinY = yValue - boundY;
	float boundMaxY = yValue + boundY;
	MPoint xyPoint(xValue, yValue, 0, 1);

	MIntArray  isNotInView;
	MPointArray viewPointList;
	int numCloseIndices = 0;

	fnMesh.getPoints(viewPointList);
	MMatrix multMatrix = meshMatrix * worldToViewMtx;
	isNotInView.setLength(viewPointList.length());
	for (int j = 0; j < (int)viewPointList.length(); j++) {

		if (SGBase::isolateVtxMap.length() && !SGBase::isolateVtxMap[j]) {
			isNotInView[j] = 1; continue;
		}

		viewPointList[j] *= multMatrix;
		viewPointList[j].x *= (aspect / viewPointList[j].w); viewPointList[j].y /= viewPointList[j].w; viewPointList[j].z = 0; viewPointList[j].w = 1;
		if (viewPointList[j].x > aspect || viewPointList[j].x < -aspect
			|| viewPointList[j].y > 1 || viewPointList[j].y < -1) {
			isNotInView[j] = 1;
		}
		else {
			isNotInView[j] = 0;
		}
	}

	double closeEdgeDist = 10000000.0;
	int    closeMeshIndex = 0;
	int    closeEdgeIndex = 0;
	MPoint closeEdgeProjected;
	float  closeEdgeParam;
	MPointArray edgePoints; edgePoints.setLength(2);

	int numEdges = fnMesh.numEdges();
	MPointArray& viewPoints = viewPointList;
	for (int j = 0; j < numEdges; j++) {
		int2 vtxList;
		fnMesh.getEdgeVertices(j, vtxList);
		if (isNotInView[vtxList[0]] && isNotInView[vtxList[1]]) continue;

		MPoint& viewPoint1 = viewPoints[vtxList[0]];
		MPoint& viewPoint2 = viewPoints[vtxList[1]];
		MPoint pointProjected;
		float param;
		double dist = SGMatrix::getPointAndVectorDist(viewPoint1, viewPoint2, xyPoint, &pointProjected, &param);

		if (dist < closeEdgeDist) {
			closeEdgeDist = dist;
			closeEdgeIndex = j;
			closeEdgeProjected = pointProjected;
			closeEdgeParam = param;
		}
	}

	int2 vtxList;
	fnMesh.getEdgeVertices(closeEdgeIndex, vtxList);
	MPointArray closeEdgePoints; closeEdgePoints.setLength(2);
	fnMesh.getPoint(vtxList[0], closeEdgePoints[0]);
	fnMesh.getPoint(vtxList[1], closeEdgePoints[1]);

	int closeIndex = 0;
	if (closeEdgeParam > 0.5) {
		closeIndex = 1;
	}

	if (viewPointList[vtxList[0]].distanceTo(closeEdgeProjected) < 0.00001 ||
		viewPointList[vtxList[1]].distanceTo(closeEdgeProjected) < 0.00001) {
		this->gotType = SGComponentType::kVertex;
		this->resultType = SGComponentType::kVertex;
		this->vtxDist = viewPointList[vtxList[closeIndex]].distanceTo(xyPoint) * height / 2.0;
		if (this->vtxDist > 10)
			this->resultType = SGComponentType::kNone;
		this->vtxIndex = vtxList[closeIndex];
		this->vtxPoint = closeEdgePoints[closeIndex] * meshMatrix;
		this->resultIndex = vtxList[closeIndex];
		this->intersectPoint = this->vtxPoint;
	}
	else {
		this->gotType = SGComponentType::kEdge;
		this->vtxIndex = vtxList[closeIndex];
		this->vtxDist = viewPointList[vtxList[closeIndex]].distanceTo(xyPoint) * height / 2.0;
		this->vtxPoint = closeEdgePoints[closeIndex] * meshMatrix;
		this->edgeIndex = closeEdgeIndex;
		this->edgeDist = closeEdgeDist * height / 2.0;
		closeEdgePoints[0] *= meshMatrix; closeEdgePoints[1] *= meshMatrix;
		this->edgePoints = closeEdgePoints;
		this->edgeParam = closeEdgeParam;
		this->intersectPoint = MVector(closeEdgePoints[1] - closeEdgePoints[0])*(double)closeEdgeParam + closeEdgePoints[0];
		if (this->vtxDist < 10) {
			this->resultIndex = this->vtxIndex;
			this->resultType = SGComponentType::kVertex;
		}
		else if (this->edgeDist < 10) {
			this->resultIndex = this->edgeIndex;
			this->resultType = SGComponentType::kEdge;
		}
		else {
			this->resultIndex = this->edgeIndex;
			this->resultType = SGComponentType::kNone;
		}
	}

	return true;
}