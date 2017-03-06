#include "precompile.h"
#include "SGMouse.h"
#include "SGPolySplitManip.h"
#include "SGIntersectFunction.h"
#include <SGSplitPoint.h>
#include <SGMesh.h>


extern SGManip* manip;

SGPolySplitManipIntersector::SGPolySplitManipIntersector()
{
	catchDist = 7;
}


void SGPolySplitManipIntersector::build()
{
}



SGPolySplitManip::SGPolySplitManip() {
	modeOn = false;
}


SGPolySplitManip::~SGPolySplitManip() {

}


void SGPolySplitManip::draw(int manipIndex) {
	if (!modeOn) return;
	if (intersectResult.oMesh.isNull()) return;
	if (intersectResult.edgeIndex == -1) return;

	SGMesh* pMesh = SGMesh::pMesh;
	MPoint intersectPoint = pMesh->getPointFromEdgeParam(intersectResult.edgeIndex, intersectResult.edgeParam, MSpace::kWorld);
	manip->pushPoint(manipIndex, intersectPoint, MColor(1, 1, 1), 5 );
}




void SGPolySplitManip::getIntersectionResult() {
	if (!modeOn) return;
	intersectResult = SGIntersectResult::getIntersectionResult(SGMouse::x, SGMouse::y, camMatrix );
}