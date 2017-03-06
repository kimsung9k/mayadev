#pragma once

#include <SGManip.h>


class SGGeneralManip
{
public:
	MPointArray getEdgeRingPoints(MDagPath dagPath, int indexEdge, const MIntArray& indicesEdge, float paramEdge);

	MMatrix camMatrix;
	int  manipNum;
	void build(const MMatrix& camMatrix);

	void drawMousePoint(int manipIndex);
	void drawDefault(int manipIndex);
	void drawEdgeParamPoint(int manipIndex);
	void drawSPoints(int manipIndex);
	void drawSplitRing(int manipIndex);
	bool getSplitPoint(int manipNum, int index, MPoint& pointOutput);
};