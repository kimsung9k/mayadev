#pragma once

#include <SGManip.h>
#include <SGShape.h>


class SGTransformManipIntersector
{
public:
	enum type {
		kNone,
		kX, kY, kZ,
		kCenter,
		kNormal,
	};

	float   catchDist;
	MVector axisX, axisY, axisZ, displayCenter;
	double axisSize;
	double coneSize;
	double centerSize;

	MPoint intersectPoint;
	SGTransformManipIntersector();
	void build(MMatrix matrix);
	void update();
	MPoint center;
	MMatrix coneXMatrix, coneYMatrix, coneZMatrix;
	MMatrix camMatrix;
	MIntArray selVertices;
	SGTransformManipIntersector::type getIntersectType();
};


class SGTransformManip
{
public:
	void draw(int manipIndex, bool hideMode = false );
	bool build();
	void update();
	void updateCenter( MPoint* pCenter = NULL );
	void getIntersectType();
	SGTransformManipIntersector intersector;
	SGTransformManipIntersector::type intersectType;
	MIntArray m_selVertices;
	bool exists();
};