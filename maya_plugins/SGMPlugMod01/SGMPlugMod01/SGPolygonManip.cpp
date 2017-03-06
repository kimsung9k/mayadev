#include "precompile.h"
#include "SGPolygonManip.h"
#include "SGIntersectFunction.h"
#include <SGMesh.h>
#include <SGIntersectResult.h>


extern SGManip* manip;

 
SGPolygonManipIntersector SGPolygonManip::intersector;
SGPolygonManipIntersector::type SGPolygonManip::intersectType;
extern vector<SGIntersectResult> generalResult;


SGPolygonManipIntersector::SGPolygonManipIntersector()
{
	arrowHeight = 7;
	arrowSpace = 10;
	arrowWidth = 20;
	catchDist = 15;
}


void SGPolygonManipIntersector::build()
{
	SGIntersectResult* pResult = &generalResult[0];
	this->dagPath = SGMesh::pMesh->dagPath;
	this->polyIndex = pResult->edgeIndex;
	update();
}


void SGPolygonManipIntersector::update()
{
	MFnMesh fnMesh = this->dagPath;
	SGMesh* pMesh = SGMesh::pMesh;
}


MPointArray SGPolygonManipIntersector::getArrowPoints(const MPoint& point1, const MPoint& point2, const MVector& dirVector) {
	MPointArray points;

	MVector edgeVector = point1 - point2;
	MPoint centerPoint = (point1 + point2) / 2;

	points.append(point1 + dirVector);
	points.append(centerPoint + dirVector / arrowSpace * arrowHeight + dirVector);
	points.append(point2 + dirVector);

	return points;
}



SGPolygonManipIntersector::type SGPolygonManipIntersector::getIntersectType(bool control)
{
	return SGPolygonManipIntersector::kNone;
}


void SGPolygonManip::draw(int manipIndex)
{
	
}


void SGPolygonManip::build()
{
	SGPolygonManip::intersector.build();
}
