#include "precompile.h"

#include "SGDragSelectionManip.h"
#include "SGMouse.h"
#include <SGMatrix.h>

extern SGManip* manip;


SGDragSelectionManip::SGDragSelectionManip() {

}


void SGDragSelectionManip::updateCamMatrix() {
	camMatrix = SGMatrix::getCamMatrix();
}


void SGDragSelectionManip::setPressPoint() {
	mousePointPress = MPoint(SGMouse::x, SGMouse::y);
}


void SGDragSelectionManip::draw(int manipIndex) {
	updateCamMatrix();

	bb.clear();
	bb.expand(mousePointPress);
	bb.expand(MPoint(SGMouse::x, SGMouse::y));

	MPoint minPoint = bb.min();
	MPoint maxPoint = bb.max();

	MPointArray points;
	points.setLength(5);
	points[0] = SGMatrix::getWorldPointFromView(MPoint(minPoint.x, minPoint.y), camMatrix);
	points[1] = SGMatrix::getWorldPointFromView(MPoint(maxPoint.x, minPoint.y), camMatrix);
	points[2] = SGMatrix::getWorldPointFromView(MPoint(maxPoint.x, maxPoint.y), camMatrix);
	points[3] = SGMatrix::getWorldPointFromView(MPoint(minPoint.x, maxPoint.y), camMatrix);
	points[4] = points[0];

	GLushort pattern = 0x5555;
	manip->pushLine(manipIndex, points, MColor(1, 1, 1), 2, &pattern);
}