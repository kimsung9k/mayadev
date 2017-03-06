#pragma once

#include <SGManip.h>
#include <SGShape.h>


class SGNormalManipIntersector
{
public:
	enum type {
		kNone,
		kNormal,
	};
	SGNormalManipIntersector();

	float   catchDist;
	double axisSize;
	double coneSize;
	double centerSize;

	bool exists;

	MPoint intersectPoint;
	void build();
	MPoint center;
	MVector normal;
	MPointArray normalLine;
	MMatrix coneMatrix;
	SGNormalManipIntersector::type getIntersectType();
};


class SGNormalManip
{
public:
	void draw(int manipIndex, bool hideMode = 0 );
	void updateCenter(MPoint* pCenter = NULL);
	void build();
	void getIntersectType();
	SGNormalManipIntersector intersector;
	SGNormalManipIntersector::type intersectType;
	MIntArray m_selVertices;
	bool exists();
};