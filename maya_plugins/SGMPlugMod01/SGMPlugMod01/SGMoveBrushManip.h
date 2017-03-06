#pragma once

#include "SGManip.h"
#include <maya/MPoint.h>


class SGMoveBrushManip
{
public:
	SGMoveBrushManip();

	void draw(int manipIndex);
	MPoint center;
	float radius;
};