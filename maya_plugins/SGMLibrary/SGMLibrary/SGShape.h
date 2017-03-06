#pragma once

#include "SGBase.h"

#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MMatrix.h>


class SGShape
{
public:
	int   numPoints;
	int   numPoly;
	int   interval;
	float* points;
	unsigned int* indices;
};



class SGCurve
{
public:
	unsigned int numPoints;
	float* points;
};



class SGConeShape
{
public:
	SGConeShape();
	~SGConeShape();
	SGShape shape;
	MVector coneDirection;
};