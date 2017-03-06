#pragma once

#include "SGManip.h"
#include <maya/MPoint.h>


class SGSoftSelectionManip
{
public:
	SGSoftSelectionManip();

	void draw(int manipIndex );
	MPoint center;
};