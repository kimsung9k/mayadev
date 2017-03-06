#pragma once

#include <maya/MDagPath.h>

class SGCam
{
public:
	SGCam();
	~SGCam();
	MDagPath m_dagPath;
};