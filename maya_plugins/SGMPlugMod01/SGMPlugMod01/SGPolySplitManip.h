#pragma once

#include <SGManip.h>
#include <SGIntersectResult.h>


class SGPolySplitManipIntersector
{
public:
	enum type {
		kNone,
		kNormal,
	};
	SGPolySplitManipIntersector();

	float   catchDist;

	MPoint intersectPoint;
	void build();
	vector<MIntArray> edgeIndices;
};


class SGPolySplitManip
{
public:
	SGPolySplitManip();
	~SGPolySplitManip();

	void draw(int manipIndex);
	void getIntersectionResult();
	SGPolySplitManipIntersector intersector;
	SGIntersectResult intersectResult;
	bool modeOn;
	MMatrix camMatrix;
};