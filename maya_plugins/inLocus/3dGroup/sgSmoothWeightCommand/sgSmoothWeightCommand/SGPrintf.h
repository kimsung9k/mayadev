#pragma once

#pragma once

#include <stdio.h>
#include <stdarg.h>
#include <maya/MGlobal.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MString.h>

void sgPrintf(const char *message, ...);
void sgPrintMatrixf(const MMatrix& matrix);
void sgPrintVectorf(const MPoint& point);