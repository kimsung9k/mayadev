#include "precompile.h"

#include "SGIntersectFunction.h"
#include "SGMouse.h"
#include <SGMatrix.h>


bool SGIntersectFunction::isPointInTriangle(const MPoint& point, const MPointArray& triangle)
{
	if (triangle.length() < 3) return false;

	MPoint tCenter = SGMatrix::getTriangleCenter(triangle);

	MVector baseLine, centerLine;
	MVector pointLine;
	for (int i = 0; i < 3; i++) {
		baseLine = triangle[(i + 1) % 3] - triangle[i];
		centerLine = tCenter - triangle[i];
		pointLine = point - triangle[i];
		MVector crossVector1 = centerLine ^ baseLine;
		MVector crossVector2 = pointLine ^ baseLine;
		if (crossVector1*crossVector2 < 0) return false;
	}
	return true;
}


double SGIntersectFunction::getShapeIntersectDist(const SGShape& targetShape, const MMatrix& shapeMatrix, const MMatrix& camMatrix)
{
	MPoint mousePoint(SGMouse::x, SGMouse::y, 0);

	MMatrix worldToView = SGMatrix::getWorldToViewMatrix(camMatrix);
	MPointArray points; points.setLength(targetShape.numPoints);
	for (int i = 0; i < targetShape.numPoints; i++) {
		float x = targetShape.points[i * 3 + 0];
		float y = targetShape.points[i * 3 + 1];
		float z = targetShape.points[i * 3 + 2];
		MPoint point(x, y, z);
		points[i] = SGMatrix::getViewPointFromWorld(point * shapeMatrix, camMatrix, &worldToView );
	}

	MIntArray indices; indices.setLength(targetShape.numPoly * targetShape.interval);
	for (int i = 0; i < targetShape.numPoly * targetShape.interval; i++){
		indices[i] = targetShape.indices[i];
	}

	double closeDist = 10000000.0;

	for (int i = 0; i < targetShape.numPoly; i++){
		int index1 = indices[i*3];
		int index2 = indices[i*3+1];
		int index3 = indices[i*3+2];

		double dist1 = SGMatrix::getLineDist(points[index1], points[index2], mousePoint);
		double dist2 = SGMatrix::getLineDist(points[index2], points[index3], mousePoint);
		double dist3 = SGMatrix::getLineDist(points[index3], points[index1], mousePoint);

		if (dist1 < closeDist) 
			closeDist = dist1;
		if (dist2 < closeDist) 
			closeDist = dist2;
		if (dist3 < closeDist)
			closeDist = dist3;
	}
	return closeDist;
}



double SGIntersectFunction::getDistWidthTriangle(const MPoint& point,
	const MPointArray& trianglePoints) {

	bool isIn = SGIntersectFunction::isPointInTriangle(point, trianglePoints);
	if (isIn) {
		return SGMatrix::getTriangleCenter(trianglePoints).distanceTo(point);
	}

	double closeDist = 10000000.0;
	for (int i = 0; i < 3; i++) {
		const MPoint& pointDst = trianglePoints[(i + 1) % 3];
		const MPoint& pointSrc = trianglePoints[i];
		double dist = SGMatrix::getLineDist(pointDst, pointSrc, point);
		if (dist < closeDist) closeDist = dist;
	}
	return closeDist;
}


double SGIntersectFunction::getLineIntersectDist(const MPoint& viewPoint, const MPointArray& line, const MMatrix& camMatrix) {
	MPoint vpLine0 = SGMatrix::getViewPointFromWorld(line[0], camMatrix);
	MPoint vpLine1 = SGMatrix::getViewPointFromWorld(line[1], camMatrix);
	return SGMatrix::getLineDist(vpLine0, vpLine1, viewPoint);
}