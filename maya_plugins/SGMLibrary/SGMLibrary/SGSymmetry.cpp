#include "precompile.h"
#include  "SGSymmetry.h"
#include "SGMatrix.h"
#include "SGPrintf.h"
#include <maya/M3dView.h>


SGSymmetry::SGSymmetry() {
	mirrorTyp = kNoMirror;
}


void SGSymmetry::setNoMirror()
{
	mirrorTyp = kNoMirror;
}


void SGSymmetry::setXMirror()
{
	mirrorTyp = kXMirror;
}


bool SGSymmetry::isNoMirror() const
{
	if (mirrorTyp == kNoMirror)
		return true;
	return false;
}


bool SGSymmetry::isXMirror() const
{
	if (mirrorTyp == kXMirror)
		return true;
	return false;
}



void SGSymmetry::convertPointToCenter(MPoint& pointToConvert)  const {
	if (mirrorTyp == kXMirror) {
		pointToConvert.x = 0;
	}
}



MPoint SGSymmetry::convertPointByMirror(const MPoint& point)  const {
	if (mirrorTyp == kXMirror) {
		return MPoint(-point.x, point.y, point.z);
	}
	return point;
}


MVector SGSymmetry::convertVectorByMirror(const MPoint& source, const MPoint& dest, const MVector& vector, bool isCenter)  const {
	if (mirrorTyp == kXMirror) {
		if (isCenter)
			return MVector(0, vector.y, vector.z);
		if ((source.x > 0 && dest.x < 0) || (source.x < 0 && dest.x > 0))
			return MVector(vector.x * -1, vector.y, vector.z);
	}
	return vector;
}



bool SGSymmetry::compairIsMirror(const MPoint& base, const MPoint& target)  const {
	if (mirrorTyp == kXMirror) {
		if ( base.x * target.x < -0.0001 ) return true;
	}
	return false;
}


MMatrix SGSymmetry::mirrorMatrix()  const {
	if (mirrorTyp == kXMirror) return xMirrorMatrix();
	return MMatrix();
}


MMatrix SGSymmetry::xMirrorMatrix() {
	double mtx[4][4] = { -1, 0, 0, 0,
		0, 1, 0, 0,
		0, 0, 1, 0,
		0, 0, 0, 1 };
	return MMatrix(mtx);
}


MMatrix SGSymmetry::yMirrorMatrix() {
	double mtx[4][4] = { 1, 0, 0, 0,
		0, -1, 0, 0,
		0, 0, 1, 0,
		0, 0, 0, 1 };
	return MMatrix(mtx);
}


MMatrix SGSymmetry::zMirrorMatrix() {
	double mtx[4][4] = { 1, 0, 0, 0,
		0, 1, 0, 0,
		0, 0, -1, 0,
		0, 0, 0, 1 };
	return MMatrix(mtx);
}


MPoint SGSymmetry::getMirroredViewPoint(const MPoint& viewPoint, const MMatrix& camMatrix )  const {
	MPoint worldPoint = SGMatrix::getWorldPointFromView(viewPoint, camMatrix);
	MPoint newViewPoint = SGMatrix::getViewPointFromWorld(worldPoint * mirrorMatrix(), camMatrix * mirrorMatrix());
	return newViewPoint;
}


MPointArray SGSymmetry::getMirroredViewPoints(const MPointArray& viewPoints, const MMatrix& camMatrix) const {
	MPointArray returnPoints;
	returnPoints.setLength(viewPoints.length());
	for (unsigned int i = 0; i < viewPoints.length(); i++) {
		returnPoints[i] = getMirroredViewPoint(viewPoints[i], camMatrix);
	}
	return returnPoints;
}