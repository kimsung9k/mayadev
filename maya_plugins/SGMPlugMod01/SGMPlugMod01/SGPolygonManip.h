#pragma once

#include <SGManip.h>


class SGPolygonManipIntersector
{
public:
	enum type {
		kNone,
		kSearching,
		kEdge,
		kExtrude,
		kBevel
	};

	SGPolygonManipIntersector();

	MDagPath dagPath;
	int polyIndex;
	double arrowSpace;
	double arrowWidth;
	double arrowHeight;

	vector<MPointArray> arrowPoints;
	MPointArray edgePoints;

	void build();
	void update();
	MPointArray getArrowPoints(const MPoint& point1, const MPoint& point2, const MVector& dirVector);
	SGPolygonManipIntersector::type getIntersectType(bool control);

	float catchDist;
};


class SGPolygonManip
{
public:
	void draw(int manipIndex);
	void build();
	static SGPolygonManipIntersector intersector;
	static SGPolygonManipIntersector::type intersectType;
};