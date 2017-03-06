#pragma once


#include <maya/MMatrix.h>

class SGSpace
{
public:
	static void setWorldSpace();
	static void setObjectSpace();
	static MSpace::Space space;
};