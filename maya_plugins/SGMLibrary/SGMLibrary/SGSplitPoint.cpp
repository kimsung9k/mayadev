#include "precompile.h"

#include "SGSplitPoint.h"
#include <maya/MMatrix.h>
#include <maya/MFnMesh.h>


SGSplitPoint::SGSplitPoint()
{
	this->typ = SGComponentType::kNone;
}


extern vector<vector<SGSplitPoint>> spPointsArr;


SGSplitPoint& SGSplitPoint::operator=(const SGSplitPoint& spPoint)
{
	this->index = spPoint.index;
	this->param = spPoint.param;
	this->point = spPoint.point;
	this->typ = spPoint.typ;

	return *this;
}


MPoint SGSplitPoint::getPoint( MSpace::Space space) {
	MFnMesh fnMesh = dagPath;
	MPoint resultPoint;
	if (typ == SGComponentType::kVertex) {
		fnMesh.getPoint(index, resultPoint, space);
	}
	else if (typ == SGComponentType::kEdge) {
		int2 vtxList;
		fnMesh.getEdgeVertices(index, vtxList);
		MPoint point1, point2;
		fnMesh.getPoint(vtxList[0], point1, space);
		fnMesh.getPoint(vtxList[1], point2, space);
		resultPoint = (point2 - point1) * (double)param + point1;
	}
	else if (typ == SGComponentType::kPolygon) {
		resultPoint = this->point;
	}
	return resultPoint;
}


bool SGSplitPoint::isCheckBasicSuccessed(int intersectIndex, const SGSplitPoint& compairObject) {
	if (!spPointsArr[intersectIndex].size()) return false;
	if (spPointsArr[intersectIndex][0].dagPath == compairObject.dagPath) {}
	else return false;
	return true;
}

bool SGSplitPoint::isStartEdge(int intersectIndex, const SGSplitPoint& compairObject) {
	if (!SGSplitPoint::isCheckBasicSuccessed(intersectIndex,compairObject)) return false;
	if (compairObject.typ == SGComponentType::kVertex) return false;

	if (spPointsArr[intersectIndex][0].typ != SGComponentType::kEdge) return false;
	if (spPointsArr[intersectIndex][0].index == compairObject.index) return true;
	return false;
}
