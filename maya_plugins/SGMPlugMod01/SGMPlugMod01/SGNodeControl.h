#pragma once


#include <maya/MPlug.h>
#include <maya/MIntArray.h>
#include <maya/MPointArray.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>


class SGNodeControl {
public:
	static MObject getObjectFromName(MString nodeName);
	static bool setPntsZero(MPlug plugPnts, MIntArray& indices, MPointArray& pnts);
	static MPlug getCurrentMeshOutputConnection(MDagPath dagPath);
	static MObject addNewNodeOnMesh(MDagPath dagPath, MString nodeType, MString nodeInputName, MString nodeOutputName);
	static MStatus deleteBeforeNode(MDagPath dagPath, MString nodeName, MString inputName);
};