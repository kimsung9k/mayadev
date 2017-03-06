#include "precompile.h"
#include "SGNormalManip.h"
#include "SGMouse.h"
#include "SGIntersectFunction.h"
#include <SGMesh.h>
#include <SGSelection.h>
#include <SGMatrix.h>
#include "SGToolCondition.h"
#include "SGPrintf.h"


extern SGManip* manip;
SGConeShape coneNormal;


SGNormalManipIntersector::SGNormalManipIntersector()
{
	catchDist = 15;
	axisSize = 50;
	coneSize = 15;
	centerSize = 10;
	normalLine.setLength(2);
}


void SGNormalManipIntersector::build()
{
	MMatrix camMatrix = SGMatrix::getCamMatrix();

	MFnMesh fnMesh = SGMesh::pMesh->dagPath;
	MIntArray selIndices = SGSelection::sels.getSelVtxIndices();
	MMatrix worldToView = SGMatrix::getWorldToViewMatrix(camMatrix);

	int targetIndex = selIndices[0];
	MPoint mousePoint(SGMouse::x, SGMouse::y);
	double closeDist = 100000.0;
	for (unsigned int i = 0; i < selIndices.length(); i++) {
		MPoint point, viewPoint;
		fnMesh.getPoint(selIndices[i], point, MSpace::kWorld);
		viewPoint = SGMatrix::getViewPointFromWorld(point, camMatrix, &worldToView);
		double dist = mousePoint.distanceTo(viewPoint);
		if (dist < closeDist) {
			closeDist = dist;
			targetIndex = selIndices[i];
		}
	}

	if (closeDist > catchDist) {
		exists = false;
		return;
	}

	fnMesh.getPoint(targetIndex, center, MSpace::kWorld);
	fnMesh.getVertexNormal(targetIndex, normal, MSpace::kWorld);
	normal.normalize();

	double manipSize = SGMatrix::getManipSizeFromWorldPoint(center, camMatrix);
	double normalSize = axisSize / manipSize;
	double coneMatrixSize = coneSize / manipSize;

	normal *= normalSize;
	normalLine.setLength(2);
	normalLine[0] = center;
	normalLine[1] = center + normal;

	MMatrix rotMatrix = SGMatrix::getRotateMatrix(MVector(0, 1, 0), normal);
	rotMatrix *= coneMatrixSize;
	rotMatrix(3, 0) = normalLine[1].x; rotMatrix(3, 1) = normalLine[1].y; rotMatrix(3, 2) = normalLine[1].z; rotMatrix(3, 3) = 1;
	coneMatrix = rotMatrix;
	exists = true;
}


SGNormalManipIntersector::type SGNormalManipIntersector::getIntersectType()
{
	if( !exists ) return SGNormalManipIntersector::kNone;
	MMatrix camMatrix = SGMatrix::getCamMatrix();
	MPoint pointSrc = SGMatrix::getViewPointFromWorld(normalLine[0], camMatrix);
	MPoint pointDst = SGMatrix::getViewPointFromWorld(normalLine[1], camMatrix);
	MPoint pointMouse(SGMouse::x, SGMouse::y);

	double lineDist = SGMatrix::getLineDist(pointSrc, pointDst, pointMouse);
	double shapeDist = SGIntersectFunction::getShapeIntersectDist(coneNormal.shape, coneMatrix, camMatrix);

	if(lineDist < catchDist || shapeDist < catchDist ) return SGNormalManipIntersector::kNormal;

	return SGNormalManipIntersector::kNone;
}



void SGNormalManip::draw( int manipIndex, bool hideMode ) {
	if (!intersector.exists) { 
		return; 
	}
	int lineWidth = 2;
	MColor color(0.1f, 0.1f, 0.9f);
	if (intersectType == SGNormalManipIntersector::kNormal)
		color = MColor(1.0f, 1.0f, 0.2f);
	
	if (!hideMode) {
		manip->pushLine(manipIndex, intersector.normalLine, color, 1);
		manip->pushShape(manipIndex, coneNormal.shape, intersector.coneMatrix, color);
	}
	else {
		GLushort linePattern = 0x5555;
		manip->pushLine(manipIndex, intersector.normalLine, color, 1, &linePattern );
	}
}



void SGNormalManip::getIntersectType()
{
	if (!exists()) {
		intersectType = SGNormalManipIntersector::kNone;
		return;
	}
	intersectType = intersector.getIntersectType();
	if( intersectType == SGNormalManipIntersector::kNone )
		intersector.build();
	intersectType = intersector.getIntersectType();
}



void SGNormalManip::updateCenter(MPoint* pCenter) {

	m_selVertices = SGSelection::getIndices(SGSelection::sels.getSelVtxIndicesMap());
	SGMesh* pMesh = SGMesh::pMesh;

	MPoint origCenter = intersector.center;
	if (pCenter == NULL)
	{
		intersector.center = SGSelection::sels.getSelectionCenter(SGToolCondition::option.symInfo );
	}
	else {
		intersector.center = *pCenter;
	}
	MPoint addPoint = intersector.center - origCenter;
	intersector.normalLine[0] += addPoint;
	intersector.normalLine[1] += addPoint;
	intersector.coneMatrix(3, 0) += addPoint.x;
	intersector.coneMatrix(3, 1) += addPoint.y;
	intersector.coneMatrix(3, 2) += addPoint.z;
}



bool SGNormalManip::exists() {
	m_selVertices = SGSelection::getIndices(SGSelection::sels.getSelVtxIndicesMap());
	if (!m_selVertices.length()) return false;
	return true;
}


void SGNormalManip::build() {
	intersector.build();
}