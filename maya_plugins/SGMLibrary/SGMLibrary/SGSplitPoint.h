#pragma once

#include "SGBase.h"
#include "SGComponentType.h"
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MPoint.h>
#include <maya/MDagPath.h>


struct SGSplitPoint
{
	MDagPath dagPath;

	SGSplitPoint();
	SGSplitPoint& operator=(const SGSplitPoint& spPoint);
	MPoint getPoint( MSpace::Space space = MSpace::kWorld );

	int index;
	float param;
	MPoint point;
	SGComponentType typ;

	static bool isCheckBasicSuccessed( int intersectIndex, const SGSplitPoint& compairObject);
	static bool isStartEdge(int intersectIndex, const SGSplitPoint& compairObject );
};