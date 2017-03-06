#pragma once

#include <stdio.h>
#include <stdarg.h>
#include <maya/MGlobal.h>
#include <vector>

#include <maya/MDagPath.h>
#include <maya/MIntArray.h>
#include <maya/MFnMesh.h>
#include <maya/MSelectionList.h>
#include <maya/MFnSet.h>
#include <maya/MFnSingleIndexedComponent.h>

using namespace std;

void SGExecuteCommand( bool undoable,  const char *message, ...);

class SGBase
{
public:
	static void getIsolateMap(const MDagPath& dagPath);
	static MIntArray isolateVtxMap;
	static MIntArray isolatePolyMap;
};
