#include "precompile.h"
#include "SGTransformManip.h"
#include "SGIntersectFunction.h"
#include "SGMouse.h"

#include <SGIntersectResult.h>
#include <SGSelection.h>
#include <SGMatrix.h>
#include <SGMesh.h>
#include <SGSpace.h>
#include <SGSymmetry.h>
#include <SGPrintf.h>

#include "SGToolCondition.h"


extern SGManip* manip;
SGConeShape cone;

extern vector<SGIntersectResult> generalResult;

SGTransformManipIntersector::SGTransformManipIntersector()
{
	catchDist = 7;
	axisSize = 50;
	coneSize = 15;
	centerSize = 10;
}


void SGTransformManipIntersector::build( MMatrix matrix )
{
	camMatrix = SGMatrix::getCamMatrix();
	center = matrix[3];
	double manipSize = SGMatrix::getManipSizeFromWorldPoint( center, camMatrix);
	double axisWorldLength = axisSize / manipSize;
	double coneWorldLength = coneSize / manipSize;
	axisX = matrix[0]; axisY = matrix[1]; axisZ = matrix[2];

	axisX = axisX.normal() * axisWorldLength;
	axisY = axisY.normal() * axisWorldLength;
	axisZ = axisZ.normal() * axisWorldLength;

	coneXMatrix = SGMatrix::getRotateMatrix( cone.coneDirection, axisX) * coneWorldLength;
	coneYMatrix = SGMatrix::getRotateMatrix( cone.coneDirection, axisY) * coneWorldLength;
	coneZMatrix = SGMatrix::getRotateMatrix( cone.coneDirection, axisZ) * coneWorldLength;
	coneXMatrix(3, 3) = 1;
	coneYMatrix(3, 3) = 1;
	coneZMatrix(3, 3) = 1;

	SGMatrix::setMatrixPosition(coneXMatrix, axisX + center);
	SGMatrix::setMatrixPosition(coneYMatrix, axisY + center);
	SGMatrix::setMatrixPosition(coneZMatrix, axisZ + center);
}

void SGTransformManipIntersector::update() {
	double manipSize = SGMatrix::getManipSizeFromWorldPoint(center, SGMatrix::getCamMatrix() );
	double axisWorldLength = axisSize / manipSize;
	double coneWorldLength = coneSize / manipSize;

	axisX = axisX.normal() * axisWorldLength;
	axisY = axisY.normal() * axisWorldLength;
	axisZ = axisZ.normal() * axisWorldLength;

	coneXMatrix = SGMatrix::getRotateMatrix(cone.coneDirection, axisX) * coneWorldLength;
	coneYMatrix = SGMatrix::getRotateMatrix(cone.coneDirection, axisY) * coneWorldLength;
	coneZMatrix = SGMatrix::getRotateMatrix(cone.coneDirection, axisZ) * coneWorldLength;
	coneXMatrix(3, 3) = 1;
	coneYMatrix(3, 3) = 1;
	coneZMatrix(3, 3) = 1;

	SGMatrix::setMatrixPosition(coneXMatrix, axisX + center);
	SGMatrix::setMatrixPosition(coneYMatrix, axisY + center);
	SGMatrix::setMatrixPosition(coneZMatrix, axisZ + center);
}



SGTransformManipIntersector::type SGTransformManipIntersector::getIntersectType()
{
	MPoint movePoint(SGMouse::x, SGMouse::y);

	MIntArray selIndices = SGSelection::getIndices(SGSelection::sels.getSelVtxIndicesMap());
	if (!selIndices.length()) return SGTransformManipIntersector::kNone;

	MMatrix camMatrix = SGMatrix::getCamMatrix();
	MPoint centerViewPoint = SGMatrix::getViewPointFromWorld(center, camMatrix);
	
	if (fabs(centerViewPoint.x - SGMouse::x) < centerSize + catchDist/2  &&
		fabs(centerViewPoint.y - SGMouse::y) < centerSize + catchDist / 2 )
		return SGTransformManipIntersector::kCenter;

	MPointArray lineX, lineY, lineZ;
	double manipSize = SGMatrix::getManipSizeFromWorldPoint(center, camMatrix);
	lineX.setLength(2); lineY.setLength(2); lineZ.setLength(2);
	lineX[0] = center; lineX[1] = center + axisX.normal() * axisSize / manipSize;
	lineY[0] = center; lineY[1] = center + axisY.normal() * axisSize / manipSize;
	lineZ[0] = center; lineZ[1] = center + axisZ.normal() * axisSize / manipSize;

	if( catchDist > SGIntersectFunction::getLineIntersectDist(movePoint, lineX, camMatrix) ||
		catchDist > SGIntersectFunction::getShapeIntersectDist(cone.shape, coneXMatrix, camMatrix)) {
		return SGTransformManipIntersector::kX;
	}
	if (catchDist > SGIntersectFunction::getLineIntersectDist(movePoint, lineY, camMatrix) ||
		catchDist > SGIntersectFunction::getShapeIntersectDist(cone.shape, coneYMatrix, camMatrix)) {
		return SGTransformManipIntersector::kY;
	}
	if (catchDist > SGIntersectFunction::getLineIntersectDist(movePoint, lineZ, camMatrix) ||
		catchDist > SGIntersectFunction::getShapeIntersectDist(cone.shape, coneZMatrix, camMatrix)) {
		return SGTransformManipIntersector::kZ;
	}

	return SGTransformManipIntersector::kNone;
}


void SGTransformManip::draw(int manipIndex, bool hideMode ) {
	double manipSize = SGMatrix::getManipSizeFromWorldPoint( intersector.center, SGMatrix::getCamMatrix() );
	double centerSize = intersector.centerSize / manipSize;

	GLushort linePattern = 0x5555;

	MColor xColor(1, 0, 0); MColor yColor(0, 1, 0); MColor zColor(0, 0, 1); MColor cColor(100/255.0f, 220/255.0f, 255/255.0f);

	if (intersectType == SGTransformManipIntersector::kCenter)
		cColor = MColor(1, 1, 0);
	else if (intersectType == SGTransformManipIntersector::kX)
		xColor = MColor(1, 1, 0);
	else if (intersectType == SGTransformManipIntersector::kY)
		yColor = MColor(1, 1, 0);
	else if (intersectType == SGTransformManipIntersector::kZ)
		zColor = MColor(1, 1, 0);

	MVector camX = SGMatrix::getCamVector(0).normal() * centerSize;
	MVector camY = SGMatrix::getCamVector(1).normal() * centerSize;
	MPointArray centerManipPoints; centerManipPoints.setLength(5);

	centerManipPoints[0] =  camX + camY + intersector.center;
	centerManipPoints[1] = -camX + camY + intersector.center;
	centerManipPoints[2] = -camX - camY + intersector.center;
	centerManipPoints[3] =  camX - camY + intersector.center;
	centerManipPoints[4] = centerManipPoints[0];

	MPointArray xLine, yLine, zLine;
	xLine.setLength(2);yLine.setLength(2);zLine.setLength(2);

	xLine[0] = intersector.center; xLine[1] = intersector.axisX + xLine[0];
	yLine[0] = intersector.center; yLine[1] = intersector.axisY + yLine[0];
	zLine[0] = intersector.center; zLine[1] = intersector.axisZ + zLine[0];

	manip->pushLine(manipIndex, xLine, xColor, 1, &linePattern);
	manip->pushLine(manipIndex, yLine, yColor, 1, &linePattern);
	manip->pushLine(manipIndex, zLine, zColor, 1, &linePattern);
	if (!hideMode) {
		manip->pushShape(manipIndex, cone.shape, intersector.coneXMatrix, xColor);
		manip->pushShape(manipIndex, cone.shape, intersector.coneYMatrix, yColor);
		manip->pushShape(manipIndex, cone.shape, intersector.coneZMatrix, zColor);
		manip->pushLine(manipIndex, centerManipPoints, cColor, 1, &linePattern);
	}
}


void SGTransformManip::getIntersectType()
{
	intersectType = intersector.getIntersectType();
}


bool SGTransformManip::build()
{
	SGIntersectResult& result = generalResult[0];
	if (result.resultType != SGComponentType::kNone) {
		intersector.intersectPoint = result.intersectPoint;
	}
	m_selVertices = SGSelection::getIndices( SGSelection::sels.getSelVtxIndicesMap() );
	if (!m_selVertices.length()) return false;

	SGMesh* pMesh = SGMesh::pMesh;

	MBoundingBox bb;
	for (unsigned int i = 0; i < m_selVertices.length(); i++) {
		MPoint& targetPoint = pMesh->points[m_selVertices[i]];
		pMesh->isCenter(m_selVertices[i], SGComponentType::kVertex);
		if( !pMesh->isCenter(m_selVertices[i], SGComponentType::kVertex ) &&
			SGToolCondition::option.symInfo.compairIsMirror( intersector.intersectPoint, targetPoint ) ) continue;
		bb.expand(targetPoint);
	}

	MPoint bbCenter = bb.center();

	if (SGSpace::space == MSpace::kObject) {
		bbCenter *= pMesh->dagPath.inclusiveMatrix();
	}

	MMatrix mtx;
	mtx(3, 0) = bbCenter.x;
	mtx(3, 1) = bbCenter.y;
	mtx(3, 2) = bbCenter.z;

	intersector.build( mtx );
	intersectType = SGTransformManipIntersector::kCenter;

	updateCenter();

	return true;
}


void SGTransformManip::updateCenter( MPoint* pCenter ) {
	SGMesh* pMesh = SGMesh::pMesh;

	MPoint center;
	if (pCenter == NULL)
	{
		center = SGSelection::sels.getSelectionCenter(SGToolCondition::option.symInfo );
	}
	else {
		center = *pCenter;
	}

	MMatrix mtx;
	mtx(3, 0) = center.x;
	mtx(3, 1) = center.y;
	mtx(3, 2) = center.z;

	intersector.build(mtx);
}


void SGTransformManip::update() {
	intersector.update();
}



bool SGTransformManip::exists() {
	m_selVertices = SGSelection::getIndices(SGSelection::sels.getSelVtxIndicesMap());
	if (!m_selVertices.length()) return false;

	return true;
}