#pragma once


#include <maya/MSelectionList.h>
#include <maya/MFnMesh.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MStringArray.h>
#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MFnCamera.h>
#include <maya/MPlug.h>
#include <maya/M3dView.h>
#include "SGCam.h"
#include "SGMesh.h"
#include "SGShaderProgram.h"
#include <vector>

using std::vector;


class SGFunctions
{
public:
	static void getCamera( SGCam* cam);
	static void getMeshs( vector<SGMesh*>& meshs );
	static void getShaders(vector<SGShaderProgram*>& shaders);
};