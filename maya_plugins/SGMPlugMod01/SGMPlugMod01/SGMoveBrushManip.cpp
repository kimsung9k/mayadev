#include "precompile.h"

#include "SGMoveBrushManip.h"
#include "SGMouse.h"
#include <SGMatrix.h>

extern SGManip* manip;

SGMoveBrushManip::SGMoveBrushManip() {
	center = MPoint(0, 0, 0);
	radius = 50.0;
}

void SGMoveBrushManip::draw(int manipIndex) {
	MMatrix camMatrix = SGMatrix::getCamMatrix();
	MPoint viewCenter = center;
	MMatrix viewToWorldMatrix = SGMatrix::getViewToWorldMatrix(camMatrix);

	float viewRadius = radius;

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
	manip->pushLine(manipIndex, points, MColor(220 / 255.0f, 220 / 255.0f, 100 / 255.0f), 2, &patten);
}