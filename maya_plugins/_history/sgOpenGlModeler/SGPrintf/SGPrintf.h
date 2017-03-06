#pragma once

#include <stdio.h>
#include <stdarg.h>
#include <maya/MGlobal.h>
#include <maya/MPoint.h>

void sgPrintf(const char *message, ...);
void sgPrintMPoint( MPoint point );