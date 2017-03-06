#pragma once

#include "SGManip.h"
#include <maya/MPoint.h>


class SGDragSelectionManip
{
public:
	SGDragSelectionManip();

	void draw(int manipIndex);

	void setPressPoint();
	void updateCamMatrix();

	MMatrix camMatrix;
	MPoint mousePointPress;

	MBoundingBox bb;
};