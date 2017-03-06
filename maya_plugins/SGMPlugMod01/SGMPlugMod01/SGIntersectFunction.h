#pragma once


#include <SGBase.h>
#include <SGShape.h>

class SGIntersectFunction
{
public:
	static bool isCenterVtx(int index);
	static double getLineIntersectDist( const MPoint& viewPoint, const MPointArray& line, const MMatrix& camMatrix);
	static double getShapeIntersectDist( const SGShape& targetShape, const MMatrix& shapeMatrix, const MMatrix& camMatrix);
	static bool isPointInTriangle(const MPoint& point, const MPointArray& triangle);
	static double getDistWidthTriangle(const MPoint& point, const MPointArray& triangle);
};