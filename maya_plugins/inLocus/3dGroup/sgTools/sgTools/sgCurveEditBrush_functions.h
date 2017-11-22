#pragma once

#include <maya/MPoint.h>
#include <maya/M3dView.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>


MPoint getViewToWorldPoint(MPoint& viewPoint);
MPoint getWorldToViewPoint(MPoint& viewPoint);