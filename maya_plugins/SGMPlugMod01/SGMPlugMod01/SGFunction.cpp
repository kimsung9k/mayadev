#include "precompile.h"
#include "SGFunction.h"
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFnTransform.h>
#include <maya/MPlug.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFnSingleIndexedComponent.h>
#include "SGMouse.h"
#include "SGCommand.h"
#include "SGTransformManip.h"
#include "SGNormalManip.h"
#include "SGSoftSelectionManip.h"
#include "SGDragSelectionManip.h"
#include "SGMoveBrushManip.h"
#include "SGNodeControl.h"
#include "SGToolCondition.h"
#include "Names.h"

#include <SGMesh.h>
#include <SGMatrix.h>
#include <SGIntersectResult.h>
#include <SGSymmetry.h>
#include <SGSelection.h>
#include <SGPrintf.h>
#include <SGBase.h>


MPoint SGFunction::origCenter;
MVector SGFunction::origNormal;
MPoint SGFunction::origCenterIntersectPoint;
SGIntersectResult SGFunction::slidingIntersector;
int SGFunction::mouseXOrig;
int SGFunction::mouseYOrig;
MPoint SGFunction::pointOffsetXY;
MPointArray SGFunction::points_before;
MPointArray SGFunction::points_after;
MFloatArray SGFunction::vertexWeights;
MFloatVectorArray SGFunction::normals_before;
MStringArray SGFunction::bevelNodes;
double SGFunction::softSelectionRadiusOrig;
double SGFunction::moveBrushRadiusOrig;

double SGFunction::slideParam;
vector<MIntArray> SGFunction::edgeGroups;
vector<vector<MPointArray>> SGFunction::edgesPoints;
MIntArray SGFunction::mergeVertexIndicesMap;

extern SGManip* manip;
extern SGTransformManip transManip;
extern SGSoftSelectionManip softSelectionManip;
extern SGDragSelectionManip dragSelectionManip;
extern SGMoveBrushManip moveBrushManip;
extern vector<SGIntersectResult> generalResult;
extern vector<vector<SGSplitPoint>> spPointsArr;
extern vector<SGIntersectResult> edgeSplitIntersectResult;
extern vector<int> snapIndexArr;

int SGFunction::getSameIndex(const MIntArray& indices1, const MIntArray& indices2) {

	int sameIndex = -1;
	for (unsigned int i = 0; i < indices1.length(); i++) {
		for (unsigned int j = 0; j < indices2.length(); j++) {
			if (indices1[i] == indices2[j]) {
				sameIndex = indices1[i]; break;
			}
		}
		if (sameIndex != -1 ) break;
	}
	return sameIndex;
}


bool SGFunction::isIn(int index, const MIntArray& indices) {
	for (unsigned int i = 0; i < indices.length(); i++) {
		if (index == indices[i]) return true;
	}
	return false;
}


MIntArray SGFunction::getPolysMap(const SGSplitPoint& spPoint, SGMesh* pMesh) {

	MIntArray polysMap;

	if (spPoint.typ == SGComponentType::kVertex) {
		polysMap = pMesh->getVtxToPolys(spPoint.index);
	}
	else if (spPoint.typ == SGComponentType::kEdge) {
		polysMap = pMesh->getEdgeToPolys(spPoint.index);
	}

	return polysMap;
}



MIntArray SGFunction::getEdgesMap(const SGSplitPoint& spPoint, SGMesh* pMesh) {

	MIntArray edgesMap;

	if (spPoint.typ == SGComponentType::kVertex) {
		edgesMap = pMesh->getVtxToEdges(spPoint.index);
	}
	else if (spPoint.typ == SGComponentType::kEdge) {
		edgesMap = pMesh->getEdgeToEdges(spPoint.index);
	}
	return edgesMap;
}



double SGFunction::getVertexParamValue(int vtxIndex, int edgeIndex, SGMesh*pMesh) {
	MIntArray vtxIndices = pMesh->getEdgeToVtxs(edgeIndex);
	if (vtxIndex == vtxIndices[0]) return 0;
	if (vtxIndex == vtxIndices[1]) return 1;
	return -1;
}


MPoint SGFunction::getWorldPointFromMousePoint( MPoint basePoint )
{
	MMatrix origCamMatrix = SGMatrix::getCamMatrix();
	MMatrix worldToViewMatrix = SGMatrix::getWorldToViewMatrix(origCamMatrix);
	MMatrix viewToWorldMatrix = worldToViewMatrix.inverse();

	MPoint viewPoint = basePoint * worldToViewMatrix;

	M3dView view = M3dView().active3dView();
	int width = view.portWidth();
	int height = view.portHeight();

	double x = (double)(SGMouse::x + pointOffsetXY.x) / width * 2 - 1;
	double y = (double)(SGMouse::y + pointOffsetXY.y) / height * 2 - 1;
	double z = viewPoint.z;

	x *= viewPoint.w;
	y *= viewPoint.w;

	return MPoint(x, y, z, viewPoint.w) * viewToWorldMatrix;
}


void SGFunction::getPointOffset( MPoint center )
{
	M3dView view = M3dView().active3dView();
	MPoint viewPoint = SGMatrix::getViewPointFromWorld(center, SGMatrix::getCamMatrix() );

	pointOffsetXY.x = viewPoint.x - SGMouse::x;
	pointOffsetXY.y = viewPoint.y - SGMouse::y;

	mouseXOrig = SGMouse::x;
	mouseYOrig = SGMouse::y;
}


void SGFunction::prepairVtxMove()
{
	if (SGMesh::pMesh->dagPath.node().isNull()) return;

	vertexWeights = SGSelection::sels.getVertexWeights();
	points_before = SGMesh::pMesh->points;
	normals_before = SGMesh::pMesh->normals;
	points_after = points_before;
	origCenter = SGSelection::sels.getSelectionCenter(SGToolCondition::option.symInfo);
	getPointOffset(origCenter);

	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;
	
	slidingIntersector.setDagPath(SGMesh::pMesh->dagPath);
	slidingIntersector.camMatrix = SGMatrix::getCamMatrix();
	slidingIntersector.getInsideIntersectionResult(SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y);
	if (slidingIntersector.isNone() || slidingIntersector.itHasOppositNormal(SGMouse::x, SGMouse::y, SGMatrix::getCamMatrix())) {
		slidingIntersector.getOutsideIntersectionResult(SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y);
	}
	origCenterIntersectPoint = slidingIntersector.intersectPoint;
	if (slidingIntersector.itHasOppositNormal(SGMouse::x, SGMouse::y, SGMatrix::getCamMatrix())) {
		MPoint afterPoint = points_after[SGSelection::sels.m_focusIndex[0]] * slidingIntersector.meshMatrix;
		origCenterIntersectPoint = getWorldPointFromMousePoint(afterPoint);
	}
	delete SGMesh::pMesh->intersector;
	SGMesh::pMesh->intersector = new MMeshIntersector();
	SGMesh::pMesh->intersector->create(SGMesh::pMesh->oSlidingBaseMesh);
}


extern SGNormalManip normalManip;
void SGFunction::prepairVtxMoveNormal()
{
	MFnMesh fnMesh(SGMesh::pMesh->dagPath);
	fnMesh.getPoints(points_before );
	fnMesh.getVertexNormals(true, normals_before );
	points_after = points_before;
	origCenter = normalManip.intersector.center;
	origNormal = normalManip.intersector.normal;
	origNormal.normalize();
	getPointOffset(origCenter);

	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;
	vertexWeights = SGSelection::sels.getVertexWeights();
}


extern SGManip* manip;
void SGFunction::vertexMove_ing()
{
	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;

	SGMesh* pMesh = SGMesh::pMesh;
	if (pMesh == NULL) return;

	if (transManip.intersectType == SGTransformManipIntersector::kX) {
		SGFunction::vertexMove_direction(MVector(1, 0, 0)); return;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kY) {
		SGFunction::vertexMove_direction(MVector(0, 1, 0)); return;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kZ) {
		SGFunction::vertexMove_direction(MVector(0, 0, 1)); return;
	}

	MFnMesh fnMesh = pMesh->dagPath;

	MPoint movePoint = getWorldPointFromMousePoint(origCenter);
	transManip.updateCenter();

	double mainWeight = SGToolCondition::option.vertexWeight;
	MVector addVector = (movePoint - origCenter)*mainWeight;

	//manip->clearManip(3);
	//manip->pushPoint(3, addVector + origCenter, MColor(1, 0, 0));

	addVector *= SGMesh::pMesh->dagPath.inclusiveMatrixInverse();
	
	MPoint compairCenter = origCenter;
	if (fabs(compairCenter.x) < 0.01) {
		compairCenter.x = 0.01;
	}
	MVector convertVector;
	MFloatArray vtxWeights = vertexWeights;
	for (unsigned int i = 0; i < vtxWeights.length(); i++) {
		if (!vtxWeights[i]) continue;
		convertVector = SGToolCondition::option.symInfo.convertVectorByMirror(compairCenter, points_before[i], addVector, pMesh->isCenter( i, SGComponentType::kVertex) );
		points_after[i] = convertVector*(double)vtxWeights[i] + points_before[i];
	}
	fnMesh.setPoints(points_after);
}


extern SGManip* manip;
void SGFunction::vertexMove_slide()
{
	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;
	if (SGMesh::pMesh->dagPath.node().isNull() ) return;

	if (transManip.intersectType == SGTransformManipIntersector::kX) {
		SGFunction::vertexMove_direction(MVector(1, 0, 0)); return;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kY) {
		SGFunction::vertexMove_direction(MVector(0, 1, 0)); return;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kZ) {
		SGFunction::vertexMove_direction(MVector(0, 0, 1)); return;
	}


	MPointOnMesh pointOnMesh;

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;
	slidingIntersector.setDagPath(SGMesh::pMesh->dagPath);
	slidingIntersector.camMatrix = SGMatrix::getCamMatrix();
	
	double mainWeight = SGToolCondition::option.vertexWeight;
	double weightedX = (SGMouse::x - mouseXOrig)* mainWeight + mouseXOrig + pointOffsetXY.x;
	double weightedY = (SGMouse::y - mouseYOrig)* mainWeight + mouseYOrig + pointOffsetXY.y;

	slidingIntersector.getInsideIntersectionResult( weightedX, weightedY );
	if (slidingIntersector.isNone() || slidingIntersector.itHasOppositNormal(weightedX, weightedY, SGMatrix::getCamMatrix())) {
		slidingIntersector.getOutsideIntersectionResult(weightedX, weightedY);
	}

	MPoint intersectPoint = slidingIntersector.intersectPoint;
	if (slidingIntersector.itHasOppositNormal(weightedX, weightedY, SGMatrix::getCamMatrix())) {
		MPoint afterPoint = points_after[SGSelection::sels.m_focusIndex[0]];
		intersectPoint = getWorldPointFromMousePoint(afterPoint);
	}
	
	MMatrix meshMatrix = SGMesh::pMesh->dagPath.inclusiveMatrix();
	MMatrix meshMatrixInv = SGMesh::pMesh->dagPath.inclusiveMatrixInverse();

	/*
	manip->clearManip(3);
	manip->pushPoint(3, origCenterIntersectPoint, MColor( 1,1,1 ) );
	manip->pushPoint(3, intersectPoint, MColor(0, 0, 1));
	/**/

	MVector addVector = intersectPoint - origCenterIntersectPoint;
	addVector *= meshMatrixInv;

	MVector convertAddVector;
	transManip.updateCenter();
	MPoint compairCenter = origCenter;
	if (fabs(compairCenter.x) < 0.01) {
		compairCenter.x = 0.01;
	}
	
	for (unsigned int i = 0; i < vertexWeights.length(); i++)
	{
		if (!vertexWeights[i]) continue;
		bool isCenter = SGMesh::pMesh->isCenter(i, SGComponentType::kVertex);
		convertAddVector = SGToolCondition::option.symInfo.convertVectorByMirror(compairCenter, points_before[i], addVector, isCenter );
		MPoint localMovePoint = (points_before[i] + convertAddVector * (double)vertexWeights[i] );
		SGMesh::pMesh->intersector->getClosestPoint(localMovePoint, pointOnMesh);
		MPoint resultPoint = MPoint(pointOnMesh.getPoint());
		points_after[i] = resultPoint;
		if (isCenter) SGToolCondition::option.symInfo.convertPointToCenter( points_after[i] );
	}
	fnMesh.setPoints(points_after);
}


void SGFunction::vertexMove_end(bool clearSelection)
{
	SGCommand::dagPathMesh = SGMesh::pMesh->dagPath;

	SGCommand::vmMoveIndices.clear();
	for (unsigned int i = 0; i < vertexWeights.length(); i++ ) {
		if ( !vertexWeights[i]) continue;
		SGCommand::vmMoveIndices.append(i);
	}

	SGCommand::vmPoints_before.setLength(SGCommand::vmMoveIndices.length());
	SGCommand::vmPoints_after.setLength(SGCommand::vmMoveIndices.length());
	for (unsigned int i = 0; i < SGCommand::vmMoveIndices.length(); i++) {
		SGCommand::vmPoints_before[i] = points_before[SGCommand::vmMoveIndices[i]];
		SGCommand::vmPoints_after[i] = points_after[SGCommand::vmMoveIndices[i]];
	}
	
	MIntArray mergeIndices;
	double maxDistance = 0.00001;
	for (int i = 0; i < generalResult.size(); i++) {
		SGIntersectResult* pResult = &generalResult[i];
		if (snapIndexArr[i] != -1) {
			int mergeIndex = snapIndexArr[i];
			mergeIndices.append(pResult->vtxIndex);
			mergeIndices.append(mergeIndex);
			MPoint& point1 = points_after[pResult->vtxIndex];
			MPoint& point2 = points_after[mergeIndex];
			if (point1.distanceTo(point2) > maxDistance) {
				maxDistance = point1.distanceTo(point2);
			}
		}
	}

	double compairDistance = 0.0001;
	if (transManip.intersectType == SGTransformManipIntersector::kCenter) {
		compairDistance = maxDistance;
	}

	MString command;
	if( mergeIndices.length() && maxDistance < 0.001 ) {
		char buffer[128];
		sprintf(buffer, "polyMergeVertex  -d %f -am 0 -ch 1 ", float(compairDistance) );
		command += buffer;
		MFnMesh fnMesh = SGMesh::pMesh->dagPath;
		MString meshName = fnMesh.partialPathName();
		char vtxName[128];
		for (unsigned int i = 0; i < mergeIndices.length(); i++) {
			sprintf(vtxName, "%s.vtx[%d] ", meshName.asChar(), mergeIndices[i]);
			command += vtxName;
		}
	}
	if (command.length()) command += (";select -cl;" + Names::commandName + " -upm;");
	if ( clearSelection ) command += "select -cl;";
	MGlobal::executeCommand(Names::commandName + " -vm;" + command, false, true);
}



int SGFunction::getSnapPointIndex(int resultIndex, MPoint pointMove)
{
	MMatrix multMatrix;
	SGIntersectResult* pResult = &generalResult[resultIndex];

	MMatrix meshMatrix = SGMesh::pMesh->dagPath.inclusiveMatrix();
	multMatrix = meshMatrix * SGMatrix::getWorldToViewMatrix(pResult->camMatrix);

	MPoint mousePoint(SGMouse::x, SGMouse::y, 0);

	int snapDist = 10;
	int boundMinX = mousePoint.x - snapDist;
	int boundMaxX = mousePoint.x + snapDist;
	int boundMinY = mousePoint.y - snapDist;
	int boundMaxY = mousePoint.y + snapDist;

	double closeDist = 1000000.0;
	MMatrix worldToView = SGMatrix::getWorldToViewMatrix(pResult->camMatrix);
	int closeIndex = -1;
	for (unsigned int i = 0; i < points_before.length(); i++) {
		MVector normal = MVector(normals_before[i]) * multMatrix;
		if (normal.z > 0) continue;
		MPoint viewPoint = SGMatrix::getViewPointFromWorld(points_before[i] * meshMatrix, pResult->camMatrix, &worldToView);
		/*if (boundMinX > viewPoint.x || boundMaxX < viewPoint.x ||
			boundMinY > viewPoint.y || boundMaxY < viewPoint.y) continue;*/
		double dist = viewPoint.distanceTo(mousePoint);
		if (dist < closeDist) {
			closeDist = dist;
			closeIndex = i;
		}
	}
	return closeIndex;
}



void SGFunction::vertexMove_snap()
{
	MPoint localOrigCenter = origCenter * SGMesh::pMesh->dagPath.inclusiveMatrixInverse();
	for (int i = 0; i < generalResult.size(); i++) {
		int snapIndex = getSnapPointIndex(i, localOrigCenter);
		snapIndexArr[i] = snapIndex;
		if (snapIndex == -1) return;
	}

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;
	SGMesh* pMesh = SGMesh::pMesh;
	MMatrix meshMatrix = pMesh->dagPath.inclusiveMatrix();
	MMatrix meshMatrixInverse = pMesh->dagPath.inclusiveMatrixInverse();
	int snapIndex = snapIndexArr[0];
	MVector addPoint = (points_before[snapIndex] - localOrigCenter)*meshMatrix;

	if (transManip.intersectType == SGTransformManipIntersector::kX) {
		addPoint.y = 0; addPoint.z = 0;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kY) {
		addPoint.x = 0; addPoint.z = 0;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kZ) {
		addPoint.x = 0; addPoint.y = 0;
	}
	else if (transManip.intersectType == SGTransformManipIntersector::kNormal) {
		MPoint movePoint = localOrigCenter;
		MPoint targetPoint = points_before[snapIndex];
		MVector targetVector = targetPoint - movePoint;
		addPoint = origNormal *(origNormal * targetVector) / pow(origNormal.length(), 2);
	}
	addPoint *= meshMatrixInverse;

	MPoint compairCenter = localOrigCenter;
	if (fabs(compairCenter.x) < 0.01) {
		compairCenter.x = 0.01;
	}
	if (transManip.intersectType == SGTransformManipIntersector::kNormal) {
		for (unsigned int i = 0; i < vertexWeights.length(); i++) {
			if (!vertexWeights[i]) continue;
			points_after[i] = MVector(addPoint)*(double)vertexWeights[i] + points_before[i];
		}
	}
	else {
		for (unsigned int i = 0; i < vertexWeights.length(); i++) {
			if (!vertexWeights[i]) continue;
			MVector convertVector = SGToolCondition::option.symInfo.convertVectorByMirror(compairCenter, points_before[i], addPoint, pMesh->isCenter(i, SGComponentType::kVertex));
			points_after[i] = convertVector*(double)vertexWeights[i] + points_before[i];
		}
	}
	fnMesh.setPoints(points_after);
	transManip.updateCenter();
}

void SGFunction::vertexMove_direction( MVector direction )
{
	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;

	SGMesh* pMesh = SGMesh::pMesh;
	if (pMesh == NULL) return;

	MPoint  point;
	MVector normal;
	if (direction.length()) {
		point = origCenter;
		normal = direction;
	}
	else {
		point = normalManip.intersector.center;
		normal = normalManip.intersector.normal;
	}
	normal.normalize();

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;

	MPoint intersectPoint = SGMatrix::getLineIntersectPoint(point, point + normal, SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y, SGMatrix::getCamMatrix() );
	
	MVector intersectVector = intersectPoint - point;
	double intersectWeight = intersectVector.length() / normal.length();
	if ( intersectVector * normal < 0 ) intersectWeight *= -1;

	/*
	sgPrintf("intersectWeight : %f", intersectWeight);
	manip->clearManip(3);
	manip->pushPoint(3, point, MColor(1, 1, 1));
	manip->pushPoint(3, point + normal * intersectWeight, MColor(1,0,0) );
	*/

	double mainWeight = SGToolCondition::option.vertexWeight;

	MPoint compairCenter = origCenter;
	if (fabs(compairCenter.x) < 0.01) {
		compairCenter.x = 0.01;
	}

	MMatrix meshMtxInverse = pMesh->dagPath.inclusiveMatrixInverse();;

	for (unsigned int i = 0; i < vertexWeights.length(); i++) {
		if (!vertexWeights[i]) continue;
		MPoint targetPoint = points_before[i];
		MPoint targetNormal;
		targetNormal = SGToolCondition::option.symInfo.convertVectorByMirror(compairCenter, points_before[i], normal * meshMtxInverse, pMesh->isCenter(i, SGComponentType::kVertex) );

		MPoint resultPoint = targetPoint + targetNormal * intersectWeight * (double)vertexWeights[i] * mainWeight;
		points_after[i] = resultPoint;
	}
	fnMesh.setPoints(points_after);
	transManip.updateCenter();
}


void SGFunction::vertexMove_normal()
{
	for (int i = 0; i < snapIndexArr.size(); i++)
		snapIndexArr[i] = -1;

	SGMesh* pMesh = SGMesh::pMesh;
	if (pMesh == NULL) return;

	MMatrix meshMatrix = pMesh->dagPath.inclusiveMatrix();
	MMatrix meshMatrixInv = pMesh->dagPath.inclusiveMatrixInverse();

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;
	MPoint intersectPoint = SGMatrix::getLineIntersectPoint(origCenter, origCenter + origNormal, SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y, SGMatrix::getCamMatrix());
	MVector intersectVector = intersectPoint - origCenter;
	double intersectWeight = (intersectVector*SGMesh::pMesh->dagPath.inclusiveMatrixInverse() ).length() / origNormal.length();
	if (intersectVector * origNormal < 0) intersectWeight *= -1;

	double allWeight = SGToolCondition::option.vertexWeight;

	for (unsigned int i = 0; i < vertexWeights.length(); i++) {
		if (!vertexWeights[i]) continue;
		MPoint targetPoint  = points_before[i];
		MPoint targetNormal = normals_before[i];

		MPoint resultPoint = targetPoint + targetNormal * intersectWeight * (double)vertexWeights[i] * allWeight;
		points_after[i] = resultPoint;
	}

	fnMesh.setPoints(points_after);
	normalManip.updateCenter();
}


MPointArray getEdgeSlidePoints(SGMesh* pMesh, int edgeIndex) {
	MPointArray edgePoints = pMesh->getEdgePoints(edgeIndex, MSpace::kWorld );
	MIntArray& baseVtxIndices = pMesh->getEdgeToVtxs(edgeIndex);
	const MIntArray& polyIndices = pMesh->getEdgeToPolys(edgeIndex);
	for (unsigned int i = 0; i < polyIndices.length(); i++) {
		const MIntArray& vtxIndices = pMesh->getPolyToVtxs(polyIndices[i]);
		for (unsigned int k = 0; k < baseVtxIndices.length(); k++) {
			for (unsigned int j = 0; j < vtxIndices.length(); j++) {
				if (baseVtxIndices[0] == vtxIndices[j] || baseVtxIndices[1] == vtxIndices[j]) continue;
				if (!pMesh->isTwoVertexHasSameEdge(baseVtxIndices[k], vtxIndices[j])) continue;
				edgePoints.append(pMesh->getPoint(vtxIndices[j], MSpace::kWorld));
			}
		}
	}
	if (edgePoints.length() == 4) {
		MPoint addPoint1 = edgePoints[0] - edgePoints[2] + edgePoints[0];
		MPoint addPoint2 = edgePoints[1] - edgePoints[3] + edgePoints[1];
		edgePoints.append(addPoint1);
		edgePoints.append(addPoint2);
	}
	return edgePoints;
}


void SGFunction::repairEdgePoints(SGMesh* pMesh, vector<MPointArray>& edgePoints, const MIntArray& edgeGroup, int rootIndex, double dotValue) {
	MPointArray& rootEdgePoints = edgePoints[rootIndex];

	MIntArray checkedMap = SGSelection::getMap(MIntArray(), pMesh->numEdges);
	MIntArray edgeToEdgeGroupIndexMap = SGSelection::getMap(MIntArray(), pMesh->numEdges );

	for (unsigned int i = 0; i < edgeGroup.length(); i++) {
		edgeToEdgeGroupIndexMap[edgeGroup[i]] = i;
	}

	int rootEdge = edgeGroup[rootIndex];
	MIntArray edgeGroupMap = SGSelection::getMap(edgeGroup, pMesh->numEdges);

	if (dotValue < 0) {
		MPoint temp1 = edgePoints[rootIndex][2];
		MPoint temp2 = edgePoints[rootIndex][3];
		edgePoints[rootIndex][2] = edgePoints[rootIndex][4];
		edgePoints[rootIndex][3] = edgePoints[rootIndex][5];
		edgePoints[rootIndex][4] = temp1;
		edgePoints[rootIndex][5] = temp2;
	}

	checkedMap[rootEdge] = 1;
	MIntArray& rootOtherEdges = pMesh->getEdgeToEdges(rootEdge);
	for (unsigned int i = 0; i < rootOtherEdges.length(); i++) {
		if (!edgeGroupMap[rootOtherEdges[i]]) continue;
		int baseEdge = rootEdge;
		int targetEdge = rootOtherEdges[i];
		while (targetEdge!=-1&&!checkedMap[targetEdge]) {
			MPointArray& baseEdgePoints = edgePoints[edgeToEdgeGroupIndexMap[baseEdge]];
			MPointArray& targetEdgePoints = edgePoints[edgeToEdgeGroupIndexMap[targetEdge]];
			int baseCloseNum = 0;
			int targetCloseNum = 0;
			if (baseEdgePoints[0] == targetEdgePoints[1]) targetCloseNum = 1;
			else if (baseEdgePoints[1] == targetEdgePoints[0]) baseCloseNum = 1;
			else if (baseEdgePoints[1] == targetEdgePoints[1]) { baseCloseNum = 1; targetCloseNum = 1;}
			MVector baseVector = baseEdgePoints[baseCloseNum + 2] - baseEdgePoints[baseCloseNum + 4];
			MVector targetVector = targetEdgePoints[targetCloseNum+2] - targetEdgePoints[targetCloseNum + 4];
			bool swap = baseVector * targetVector < 0;
			if (swap ) {
				MPoint temp1 = targetEdgePoints[2];
				MPoint temp2 = targetEdgePoints[3];
				targetEdgePoints[2] = targetEdgePoints[4];
				targetEdgePoints[3] = targetEdgePoints[5];
				targetEdgePoints[4] = temp1;
				targetEdgePoints[5] = temp2;
			}
			MIntArray& targetOtherEdges = pMesh->getEdgeToEdges(targetEdge);
			int targetEdgeNext = -1;
			for (unsigned int j = 0; j < targetOtherEdges.length(); j++) {
				if (!edgeGroupMap[targetOtherEdges[j]]) continue;
				if (baseEdge == targetOtherEdges[j]) continue;
				targetEdgeNext = targetOtherEdges[j];
			}
			baseEdge = targetEdge;
			targetEdge = targetEdgeNext;
			checkedMap[baseEdge] = 1;
		}
	}
}



void SGFunction::prepairEdgeMove()
{
	if (edgeSplitIntersectResult[0].resultType == SGComponentType::kNone) return;
	 SGMesh* pMesh = SGMesh::pMesh;
	getPointOffset(edgeSplitIntersectResult[0].intersectPoint);

	MFnMesh fnMesh(SGMesh::pMesh->dagPath);
	fnMesh.getPoints(points_before);
	points_after = points_before;

	MIntArray selIndicesMap = SGSelection::sels.getSelEdgeIndicesMap();
	
	MIntArray edgeIndices = SGSelection::getIndices(selIndicesMap);

	edgeGroups = SGSelection::getEdgeLoopGroupByIndicesMap( selIndicesMap );
	edgesPoints.resize(edgeGroups.size());

	MPoint edgeCenter = pMesh->getEdgeCenter(edgeSplitIntersectResult[0].edgeIndex, MSpace::kWorld);
	MPointArray slidePoints = getEdgeSlidePoints(pMesh, edgeSplitIntersectResult[0].edgeIndex);
	MPoint positivePoint = (slidePoints[2] + slidePoints[3]) / 2.0;
	MVector directionVector = positivePoint - edgeCenter;

	MPoint center, positive;
	MVector direction;
	
	vertexWeights = SGSelection::sels.getVertexWeights();

	MPoint compairCenter = edgeCenter;
	if (fabs(compairCenter.x) < 0.01) {
		compairCenter.x = 0.01;
	}
	mergeVertexIndicesMap = SGSelection::getMap( MIntArray(), pMesh->numVertices );
	for (int i = 0; i < edgeGroups.size(); i++) {
		double maxDotValue = 0;
		int maxDotIndex;
		edgesPoints[i].resize( edgeGroups[i].length() );
		for (unsigned int j = 0; j < edgeGroups[i].length(); j++) {
			edgesPoints[i][j] = getEdgeSlidePoints(pMesh, edgeGroups[i][j] );
			center = (edgesPoints[i][j][0] + edgesPoints[i][j][1]) / 2.0;
			positive = (edgesPoints[i][j][2] + edgesPoints[i][j][3]) / 2.0;
			direction = positive - center;
			MVector convert = SGToolCondition::option.symInfo.convertVectorByMirror(compairCenter, center, directionVector, false);

			double dotValue = convert.normal() * direction.normal();
			if (fabs(dotValue) > fabs(maxDotValue)) {
				maxDotValue = dotValue;
				maxDotIndex = j;
			}
		}
		repairEdgePoints(pMesh, edgesPoints[i], edgeGroups[i], maxDotIndex, maxDotValue);
	}
	for (int i = 0; i < edgeGroups.size(); i++) {
		for (unsigned int j = 0; j < edgeGroups[i].length(); j++) {
			MIntArray& edgeToPolys = pMesh->getEdgeToPolys(edgeGroups[i][j]);
			for (unsigned int k = 0; k < edgeToPolys.length(); k++) {
				MIntArray& polyToVtxs = pMesh->getPolyToVtxs(edgeToPolys[k]);
				for (unsigned int m = 0; m < polyToVtxs.length(); m++) {
					mergeVertexIndicesMap[polyToVtxs[m]] = 1;
				}
			}
		}
	}
	slideParam = 0;
}

extern SGManip* manip;
void SGFunction::edgeMove_slide() {
	SGMesh* pMesh = SGMesh::pMesh;

	MPoint edgeCenter = pMesh->getEdgeCenter(edgeSplitIntersectResult[0].edgeIndex, MSpace::kWorld);
	MPointArray slidePoints = getEdgeSlidePoints(pMesh, edgeSplitIntersectResult[0].edgeIndex);
	MPoint positivePoint = (slidePoints[2] + slidePoints[3]) / 2.0;
	MPoint negativePoint = (slidePoints[4] + slidePoints[5]) / 2.0;
	MVector directionVector = positivePoint - edgeCenter;

	MPoint pointIntersectP = SGMatrix::getLineIntersectPoint(edgeCenter, positivePoint, SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y, SGMatrix::getCamMatrix());
	MVector vectorIntersectP = pointIntersectP - edgeCenter;

	/*
	manip->clearManip(3);
	MPointArray points; points.setLength(2);
	points[0] = edgeCenter;
	points[1] = positivePoint;
	manip->pushPoint(3, edgeCenter, MColor(1, 0, 0));
	manip->pushLine(3, points, MColor(1, 1, 0));
	/**/

	double paramP = vectorIntersectP.length()/directionVector.length();
	if (paramP > 1) paramP = 1;
	slideParam = paramP;
	double paramN = 0;
	if (directionVector*vectorIntersectP < 0){
		paramP = 0;
		MPoint pointIntersectN = SGMatrix::getLineIntersectPoint(edgeCenter, negativePoint, SGMouse::x + pointOffsetXY.x, SGMouse::y + pointOffsetXY.y, SGMatrix::getCamMatrix());
		MVector vectorIntersectN = pointIntersectN - edgeCenter;
		paramN = vectorIntersectN.length() / (negativePoint- edgeCenter).length();
		if (paramN > 1) paramN = 1;
		slideParam = paramN;
	}

	MIntArray addMap = SGSelection::getMap(MIntArray(), pMesh->numVertices);
	MPointArray pointsAdd; pointsAdd.setLength(pMesh->numVertices);
	for (int i = 0; i < edgeGroups.size(); i++) {
		for (unsigned int j = 0; j < edgeGroups[i].length(); j++) {
			MIntArray& vtxList = pMesh->getEdgeToVtxs(edgeGroups[i][j]);
			addMap[vtxList[0]] += 1;
			addMap[vtxList[1]] += 1;
			pointsAdd[vtxList[0]] = MPoint(0, 0, 0);
			pointsAdd[vtxList[1]] = MPoint(0, 0, 0);
		}
	}

	for (int i = 0; i < edgeGroups.size(); i++) {
		for (unsigned int j = 0; j < edgeGroups[i].length(); j++) {
			MIntArray& vtxList = pMesh->getEdgeToVtxs(edgeGroups[i][j]);
			if (paramP != 0) {
				pointsAdd[vtxList[0]] += (edgesPoints[i][j][2] - edgesPoints[i][j][0]) * (double)paramP;
				pointsAdd[vtxList[1]] += (edgesPoints[i][j][3] - edgesPoints[i][j][1]) * (double)paramP;
			}
			else if (paramN != 0) {
				pointsAdd[vtxList[0]] += (edgesPoints[i][j][4] - edgesPoints[i][j][0]) * (double)paramN;
				pointsAdd[vtxList[1]] += (edgesPoints[i][j][5] - edgesPoints[i][j][1]) * (double)paramN;
			}
		}
	}

	MMatrix mtxInv = pMesh->dagPath.inclusiveMatrixInverse();
	for (unsigned int i = 0; i < addMap.length(); i++) {
		if (!addMap[i]) continue;
		points_after[i] = points_before[i] + (pointsAdd[i] / addMap[i])*mtxInv;
	}

	MFnMesh fnMesh = pMesh->dagPath;
	fnMesh.setPoints(points_after);
}


void SGFunction::edgeMove_end(bool clearSelection) {
	if (edgeSplitIntersectResult[0].resultType == SGComponentType::kNone) {
		return;
	}

	SGCommand::dagPathMesh = SGMesh::pMesh->dagPath;
	SGCommand::vmMoveIndices.clear();
	for (unsigned int i = 0; i < vertexWeights.length(); i++) {
		if (!vertexWeights[i]) continue;
		SGCommand::vmMoveIndices.append(i);
	}

	SGCommand::vmPoints_before.setLength(SGCommand::vmMoveIndices.length());
	SGCommand::vmPoints_after.setLength(SGCommand::vmMoveIndices.length());
	for (unsigned int i = 0; i < SGCommand::vmMoveIndices.length(); i++) {
		SGCommand::vmPoints_before[i] = points_before[SGCommand::vmMoveIndices[i]];
		SGCommand::vmPoints_after[i] = points_after[SGCommand::vmMoveIndices[i]];
	}

	MIntArray mergeIndices;

	if (fabs(slideParam) == 1) {
		for (unsigned int i = 0; i < mergeVertexIndicesMap.length(); i++) {
			if (!mergeVertexIndicesMap[i]) continue;
			mergeIndices.append(i);
		}
	}

	double compairDistance = 0.001;

	MString command;
	if (mergeIndices.length()) {
		char buffer[128];
		sprintf(buffer, "polyMergeVertex  -d %f -am 0 -ch 1 ", float(compairDistance));
		command += buffer;
		MFnMesh fnMesh = SGMesh::pMesh->dagPath;
		MString meshName = fnMesh.partialPathName();
		char vtxName[128];
		for (unsigned int i = 0; i < mergeIndices.length(); i++) {
			sprintf(vtxName, "%s.vtx[%d] ", meshName.asChar(), mergeIndices[i]);
			command += vtxName;
		}
	}
	if (command.length()) command += (";select -cl;" + Names::commandName + " -upm;");
	if (clearSelection) command += ";select -cl;";
	MGlobal::executeCommand(Names::commandName + " -vm;" + command, false, true);
}



void SGFunction::clearSplitPoint()
{
	for (int i = 0; i < spPointsArr.size(); i++) {
		spPointsArr[i].clear();
	}
}


extern vector<SGIntersectResult> edgeSplitIntersectResult;
void SGFunction::pushSplitPoint()
{
	for (int i = 0; i < edgeSplitIntersectResult.size(); i++) {
		SGIntersectResult* pResult = &edgeSplitIntersectResult[i];
		 SGMesh* pMesh = SGMesh::pMesh;

		SGSplitPoint newSplitPoint;
		newSplitPoint.dagPath = SGMesh::pMesh->dagPath;
		newSplitPoint.typ = pResult->resultType;
		newSplitPoint.index = pResult->resultIndex;
		newSplitPoint.param = pResult->edgeParam;

		//sgPrintf("result type and index : %d, %d", newSplitPoint.typ, newSplitPoint.index);

		if (spPointsArr[i].size()) {
			int lastIndex = (int)spPointsArr[i].size() - 1;
			bool hasRelation = pMesh->isTwoSplitPointsHasRelation(spPointsArr[i][lastIndex], newSplitPoint);
			if (hasRelation) {
				bool hasSameEdge = pMesh->isTwoSplitPointsHasSameEdge(spPointsArr[i][lastIndex], newSplitPoint);
				if (hasSameEdge) spPointsArr[i].pop_back();
			}
			if (newSplitPoint.typ == SGComponentType::kVertex) {
				MIntArray indices; MFloatArray params;
				pMesh->getSplitEdgesAndParams(spPointsArr[i][lastIndex], newSplitPoint, indices, params);
				newSplitPoint.typ = SGComponentType::kEdge;
				newSplitPoint.index = indices[1];
				newSplitPoint.param = params[1];
			}
		}
		spPointsArr[i].push_back(newSplitPoint);
	}
}


void SGFunction::editSplitPoint()
{
	for (int i = 0; i < edgeSplitIntersectResult.size(); i++) {
		SGIntersectResult* pResult = &edgeSplitIntersectResult[i];
		if (pResult->resultType == SGComponentType::kEdge)
		{
			pResult->updateParameter(SGMouse::x, SGMouse::y, NULL);
			int lastIndex = (int)spPointsArr[i].size() - 1;
			spPointsArr[i][lastIndex].param = pResult->edgeParam;

			if (SGSplitPoint::isStartEdge(i, spPointsArr[i][lastIndex]) && spPointsArr[i].size() > 1) {
				spPointsArr[i][0] = spPointsArr[i][lastIndex];
			}
		}
		else if (pResult->resultType == SGComponentType::kPolygon) {
			/*
			int lastIndex = (int)spPointsArr[i].size() - 1;

			MMatrix camMatrix = SGMatrix::getCamMatrix();
			if ( i == 1 && SGToolCondition::option.symInfo.isXMirror() ) {
				camMatrix *= SGToolCondition::option.symInfo.mirrorMatrix();
			}
			edgeSplitIntersectResult[i] = SGIntersectResult::getIntersectionResult(SGMouse::x, SGMouse::y, camMatrix);
			edgeSplitIntersectResult[i].resultType = SGComponentType::kPolygon;
			edgeSplitIntersectResult[i].resultIndex = edgeSplitIntersectResult[i].polyIndex;

			spPointsArr[i][lastIndex].index = pResult->polyIndex;
			spPointsArr[i][lastIndex].point = pResult->intersectPoint;*/
		}
	}
}



void getEdgeAndParamFromNext(SGSplitPoint spPoint, SGSplitPoint spPointNext, 
	int& edgeIndex, float& param )
{
	if (spPoint.typ == SGComponentType::kEdge) {
		edgeIndex = spPoint.index;
		param = spPoint.param;
		return;
	}
	SGMesh* pMesh = SGMesh::pMesh;
	MIntArray nextPolyIndices = pMesh->getPolysMap(spPoint);

	MIntArray polysMap     = SGFunction::getPolysMap(spPoint, pMesh);
	MIntArray polysMapNext = SGFunction::getPolysMap(spPointNext, pMesh);
	int samePolyIndex = SGFunction::getSameIndex(polysMap, polysMapNext);

	if (samePolyIndex == -1) {
		if (pMesh->numVertices-1 < spPoint.index) {
			edgeIndex = -1;
			param = 0;
		}
		else {
			MIntArray& edges = pMesh->getVtxToEdges(spPoint.index);
			edgeIndex = edges[0];
			param = 0;
		}
		return;
	}

	MIntArray& samePolyEdges = pMesh->getPolyToEdges(samePolyIndex);
	MIntArray edgesMap     = SGFunction::getEdgesMap(spPoint, pMesh);

	edgeIndex = SGFunction::getSameIndex(samePolyEdges, edgesMap);
	param = SGFunction::getVertexParamValue( spPoint.index, edgeIndex, pMesh);
}


void SGFunction::splitEdge()
{
	int numIntersect = (int)spPointsArr.size();

	if (spPointsArr[0].size() < 2) {
		for (int i = 0; i < numIntersect; i++) {
			spPointsArr[i].clear();
		}
		return;
	}

	SGMesh* pMesh = SGMesh::pMesh;
	MString allCommand = Names::commandName + " -upm;select -cl;";
	for (int i = 0; i < numIntersect; i++) {
		MString commandString = "polySplit - ch 1 - sma 180 ";
		int numSpPoint = (int)spPointsArr[i].size();
		for (int j = 0; j < numSpPoint; j++) {
			char buffer[256]; buffer[0] = '\0';
			if (spPointsArr[i][j].typ == SGComponentType::kEdge) {
				if (i != 0 && spPointsArr[0][j].index == spPointsArr[i][j].index && spPointsArr[i][j].param != 0)
					sprintf(buffer, "-ep %d %f ", spPointsArr[i][j].index, 1.0f);
				else
					sprintf(buffer, "-ep %d %f ", spPointsArr[i][j].index, spPointsArr[i][j].param);
			}
			else if( spPointsArr[i][j].typ == SGComponentType::kVertex ){
				int targetEdge = -1;
				double targetParam = 0;
				MIntArray& edges = pMesh->getVtxToEdges(spPointsArr[i][j].index);
				for (unsigned int k = 0; k < edges.length(); k++) {
					MIntArray& vtxs = pMesh->getEdgeToVtxs(edges[k]);
					if (vtxs[0] == spPointsArr[i][j].index) {
						targetEdge = edges[k]; break;
					}
				}
				if (targetEdge == -1) {
					targetEdge = edges[0];
					targetParam = 1;
				}
				sprintf(buffer, "-ep %d %f ", targetEdge, targetParam);
			}
			else if (spPointsArr[i][j].typ == SGComponentType::kPolygon) {
				sprintf(buffer, "-fp %d %f %f %f ", spPointsArr[i][j].index, spPointsArr[i][j].point.x, spPointsArr[i][j].point.y, spPointsArr[i][j].point.z );
			}
			commandString += buffer;
		}
		commandString += (MFnMesh(spPointsArr[0][0].dagPath).partialPathName() + ";");
		allCommand += commandString;
	}
	allCommand = allCommand + Names::commandName + " -upm;";
	MGlobal::executeCommand(allCommand, false, true);

	for (int i = 0; i < numIntersect; i++) {
		spPointsArr[i].clear();
	}
}


void SGFunction::deleteComponent()
{
	SGIntersectResult* pResult = &generalResult[0];
	MDagPath targetDagPath = SGMesh::pMesh->dagPath;
	
	MString meshName = MFnMesh(targetDagPath).partialPathName();
	
	MIntArray edgeIndices = SGSelection::sels.getSelEdgeIndices();
	MIntArray polyIndices = SGSelection::sels.getSelPolyIndices();

	MString allCommand;
	if (polyIndices.length()) {
		MGlobal::executeCommand(Names::commandName + " -upm;" + "doDelete;" + Names::commandName + " -upm;", true, true);
	}
	else if (edgeIndices.length()) {
		MGlobal::executeCommand(Names::commandName + " -upm;" + "DeleteEdge;" + Names::commandName + " -upm;", true, true);
	}
}



void SGFunction::setSelection()
{
	SGSelection::sels.select(generalResult, 0);
}


void SGFunction::ifNewSetSelection() {
	if (SGSelection::sels.m_focusType.size() && generalResult[0].resultType == SGSelection::sels.m_focusType[0] ) {
		MIntArray indicesMap = SGSelection::sels.getSelIndicesMap( generalResult[0].resultType );
		if (indicesMap.length() > (unsigned int )generalResult[0].resultIndex && !indicesMap[generalResult[0].resultIndex]) {
			SGSelection::sels.select(generalResult, 0);
		}
	}
	else
		SGSelection::sels.select(generalResult, 0);
}



void SGFunction::addSelection()
{
	SGSelection::sels.select(generalResult,1);
}


void SGFunction::addDbClickSelection()
{
	SGSelection::sels.addDBClickSelection(generalResult);
}


void SGFunction::clearSelection(bool excuteCommand) {
	SGSelection::sels.clearSelection();
}


void SGFunction::selectionGrow() {
	SGSelection::sels.growSelection();
}


void SGFunction::selectionReduce() {
	SGSelection::sels.reduceSelection();
}



void SGFunction::prepairSoftSelection() {
	mouseXOrig = SGMouse::x; mouseYOrig = SGMouse::y;
	softSelectionManip.center = SGSelection::sels.getSelectionCenter(SGToolCondition::option.symInfo);
	MGlobal::executeCommand("softSelect -softSelectEnabled true;");
	MGlobal::executeCommand("softSelect -q -ssd;", softSelectionRadiusOrig);
}



void SGFunction::editSoftSelection() {
	double manipSize = SGMatrix::getManipSizeFromWorldPoint(softSelectionManip.center, SGMatrix::getCamMatrix());
	double addValue = (SGMouse::x - mouseXOrig) / manipSize;
	double value = softSelectionRadiusOrig + addValue;
	char buffer[128];
	sprintf(buffer, "softSelect -e -ssd %f", value );
	MGlobal::executeCommand(buffer);
}


void SGFunction::setSoftSelection() {
	double cuValue;
	MGlobal::executeCommand("softSelect -q -ssd;", cuValue);
	char buffer[128];
	sprintf(buffer, "softSelect -e -ssd %f", softSelectionRadiusOrig);
	MGlobal::executeCommand(buffer);
	sprintf(buffer, "softSelect -e -ssd %f", cuValue);
	MGlobal::executeCommand(buffer, false, true);
}


void SGFunction::toggleSoftSelection() {
	int result;
	MGlobal::executeCommand("softSelect -q -sse;", result);
	if (result) {
		MGlobal::executeCommand("softSelect -e -sse 0;", false, true);
	}
	else {
		MGlobal::executeCommand("softSelect -e -sse 1;", false, true);
	}
}


void SGFunction::updateMoveBrushCenter() {
	moveBrushManip.center.x = SGMouse::x;
	moveBrushManip.center.y = SGMouse::y;
}



void SGFunction::prepairMoveBrushRadius() {
	mouseXOrig = SGMouse::x; mouseYOrig = SGMouse::y;
	moveBrushManip.center.x = mouseXOrig;
	moveBrushManip.center.y = mouseYOrig;
	moveBrushRadiusOrig = moveBrushManip.radius;
}



void SGFunction::editMoveBrushRadius() {
	double addValue = SGMouse::x - mouseXOrig;
	moveBrushManip.radius = moveBrushRadiusOrig + addValue;
	sgPrintf("move brush radius edit : %f", moveBrushManip.radius);
}


void SGFunction::editSplitRingPoint()
{
	for (int i = 0; i < edgeSplitIntersectResult.size(); i++) {
		SGIntersectResult* pResult = &edgeSplitIntersectResult[i];
		if (pResult->resultType == SGComponentType::kNone) return;

		SGMesh* pMesh = SGMesh::pMesh;
		pResult->updateParameter(SGMouse::x, SGMouse::y, NULL);
	}
}


void SGFunction::polySplitRing()
{
	SGIntersectResult* pResult = &edgeSplitIntersectResult[0];
	if (pResult->edgeParam == 1 || pResult->edgeParam == 0) return;
	SGCommand::dagPathMesh = SGMesh::pMesh->dagPath;
	SGMesh* pMesh = SGMesh::pMesh;

	int size = (int)edgeSplitIntersectResult.size();

	MString allCommand = Names::commandName + " -upm;";
	for (int i = 0; i < size; i++) {
		SGIntersectResult* pResult = &edgeSplitIntersectResult[i];
		MIntArray edgeRings = pMesh->getEdgeRing(pResult->edgeIndex);
		int       rootEdge = pResult->edgeIndex;
		double     weight = pResult->edgeParam;

		MString selectCommand = "select ";

		MFnMesh fnMesh = SGMesh::pMesh->dagPath;
		for (unsigned int j = 0; j < edgeRings.length(); j++) {
			char buffer[128];
			sprintf( buffer, "%s.e[%d] ", fnMesh.partialPathName().asChar(), edgeRings[j] );
			selectCommand += buffer;
		}
		selectCommand += ";";

		char polysplitRingCommand[256];
		sprintf(polysplitRingCommand, "polySplitRing - ch on - splitType 1 - rootEdge %d - weight %f - smoothingAngle 30 - fixQuads 1 - insertWithEdgeFlow 0;", rootEdge, weight);

		allCommand += selectCommand;
		allCommand += polysplitRingCommand;
		allCommand += "select -cl;";

		bool centerExists = false;
		for (unsigned int j = 0; j < edgeRings.length(); j++) {
			MPointArray points = pMesh->getEdgePoints(edgeRings[j], MSpace::kObject );
			MIntArray& edgeToVtxs = pMesh->getEdgeToVtxs(edgeRings[j]);
			if (fabs(points[0].x) < 0.001 && fabs(points[1].x) < 0.001) {
				centerExists = true; break;
			}
		}
		if (centerExists) break;
	}
	
	allCommand = allCommand + Names::commandName + " -upm;";
	MGlobal::executeCommand(allCommand, false, true);

	for (int i = 0; i < edgeSplitIntersectResult.size(); i++)
		edgeSplitIntersectResult[i].clearResult();
}



void SGFunction::setCamFocus()
{
	MPoint centerPoint;

	if (SGSelection::sels.selExists()) {
		centerPoint = SGSelection::sels.getSelectionCenter(SGToolCondition::option.symInfo);
	}
	else {
		SGIntersectResult* pResult = &generalResult[0];
		if (pResult->resultType == SGComponentType::kNone) return;

		if (pResult->resultType.typ == SGComponentType::kVertex) {
			centerPoint = pResult->vtxPoint;
		}
		else if (pResult->resultType.typ == SGComponentType::kEdge) {
			MPointArray points = pResult->edgePoints;
			centerPoint = (points[0] + points[1]) / 2;
		}
		else if (pResult->resultType.typ == SGComponentType::kPolygon) {
			MBoundingBox bbox;
			for (unsigned int i = 0; i < pResult->polyPoints.length(); i++) {
				bbox.expand(pResult->polyPoints[i]);
			}
			centerPoint = bbox.center();
		}
	}

	MPoint camPos = SGMatrix::getCamPos();
	MVector camVector = SGMatrix::getCamVector();
	MVector centerVector = centerPoint - camPos;
	MVector projVector = camVector * ( (centerVector * camVector) / pow(camVector.length(), 2) );
	MVector moveVector = centerVector - projVector;

	M3dView activeView = M3dView().active3dView();
	MDagPath camDagPath;
	activeView.getCamera(camDagPath);

	MFnDagNode dagCam = camDagPath;
	MDagPath parentDagPath = MDagPath::getAPathTo(dagCam.parent(0));
	MFnTransform trCam = parentDagPath;
	trCam.setTranslation( camPos + moveVector, MSpace::kWorld );
	MPlug plugCoi = dagCam.findPlug("centerOfInterest");
	plugCoi.setDouble((projVector * camDagPath.exclusiveMatrixInverse()).length());
}



void SGFunction::bevelEdge() {
	SGIntersectResult* pResult = &generalResult[0];
	if (pResult->resultType == SGComponentType::kNone) return;
	 SGMesh* pMesh = SGMesh::pMesh;

	if (!bevelNodes.length()) {
		getPointOffset(pResult->intersectPoint);
		MString commandString = "polyBevel -ch 1 -offset 0";
		MFnMesh fnMesh = SGMesh::pMesh->dagPath;
		MIntArray edgesMap = SGSelection::sels.getSelEdgeIndicesMap();
		SGCommand::bvlIndices.clear();
		for (unsigned int i = 0; i < edgesMap.length(); i++) {
			if (!edgesMap[i]) continue;
			char buffer[256];
			SGCommand::bvlIndices.append(i);
			sprintf(buffer, "%s.e[%d] ", fnMesh.partialPathName().asChar(), i );
			commandString += buffer;
		}
		MGlobal::executeCommand(commandString, bevelNodes, false, false);
		SGCommand::dagPathMesh = SGMesh::pMesh->dagPath;
	}
	else {
		M3dView().active3dView().refresh(false, true);
		MPointArray edgePoints = pMesh->getEdgePoints(pResult->edgeIndex, MSpace::kWorld);
		MPoint centerPoint = (edgePoints[0] + edgePoints[1]) / 2;
		MPoint movePoint = getWorldPointFromMousePoint(centerPoint);
		double offsetValue = SGMatrix::getLineDist(edgePoints[0], edgePoints[1], movePoint);

		MSelectionList selList;
		MObject oNode;
		selList.add(bevelNodes[0]);
		selList.getDependNode(0, oNode);
		MFnDependencyNode fnNode = oNode;
		MPlug plugOffset = fnNode.findPlug("offset");
		plugOffset.setFloat(offsetValue);

		SGCommand::bvlOffset = offsetValue;
	}
}


void SGFunction::bevelEdgeFinish() {
	SGIntersectResult* pResult = &generalResult[0];
	SGNodeControl::deleteBeforeNode(SGMesh::pMesh->dagPath, "polyBevel2", "inputPolymesh");
	MGlobal::executeCommand(Names::commandName + " -bvl", false, true);
	bevelNodes.clear();
}


void SGFunction::dragSelectionPress() {
	dragSelectionManip.setPressPoint();
}



void SGFunction::dragSelectionDrag() {
}


void SGFunction::dragSelectionRelease(bool shift, bool ctrl) {

	MBoundingBox bb;
	MPoint point1 = dragSelectionManip.mousePointPress;
	MPoint point2 = MPoint(SGMouse::x, SGMouse::y);

	MPointArray points;
	points.setLength(5);
	points[0] = point1;
	points[1] = MPoint(point1.x, point2.y);
	points[2] = point2;
	points[3] = MPoint(point2.x, point1.y);
	points[4] = points[0];

	unsigned short selType = 0;
	if (shift && !ctrl) selType = 1;
	else if (!shift && ctrl) selType = 2;
	else if (shift && ctrl) selType = 3;

	SGBase::getIsolateMap(SGMesh::pMesh->dagPath);
	SGSelection::sels.dragSelection(generalResult, points, SGMatrix::getCamMatrix(), SGToolCondition::option.symInfo, selType);
}