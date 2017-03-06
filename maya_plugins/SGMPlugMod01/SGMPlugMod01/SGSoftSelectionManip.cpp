#include "precompile.h"

#include "SGSoftSelectionManip.h"
#include "SGMouse.h"
#include <SGMatrix.h>

extern SGManip* manip;

SGSoftSelectionManip::SGSoftSelectionManip() {
	center = MPoint(0, 0, 0);
}

void SGSoftSelectionManip::draw(int manipIndex) {
	MMatrix camMatrix = SGMatrix::getCamMatrix();
	float manipSize = SGMatrix::getManipSizeFromWorldPoint(center, camMatrix);
	MPoint viewCenter = SGMatrix::getViewPointFromWorld(center, camMatrix);
	MMatrix viewToWorldMatrix = SGMatrix::getViewToWorldMatrix(camMatrix);

	double radius;
	MGlobal::executeCommand("softSelect -q -ssd;", radius);
	float viewRadius = radius * manipSize;

	int pointDetail = 360;
	int x, y;
	float eachParam = 3.14159 * 2 / pointDetail;
	MPointArray points; points.setLength(pointDetail);
	for (unsigned int i = 0; i < 360; i++) {
		x = viewCenter.x + sin(eachParam*i) * viewRadius;
		y = viewCenter.y + cos(eachParam*i) * viewRadius;
		MPoint viewPoint(x, y, 0);
		points[i] = SGMatrix::getWorldPointFromView(viewPoint, camMatrix, &viewToWorldMatrix);
	}
	GLushort patten = 0x5555;
	manip->pushLine(manipIndex, points, MColor(100/255.0f, 220 / 255.0f, 1), 2, &patten);
}