#pragma once

#include <maya/MPxNode.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MTypeId.h>
#include <maya/MDataHandle.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MPoint.h>
#include <maya/MPointArray.h>

#include <maya/MFnMesh.h>
#include <maya/MGlobal.h>

#include <maya/MFnMeshData.h>

class sgModifiedMeshKeeper : public MPxNode
{
public:
	sgModifiedMeshKeeper();
	virtual ~sgModifiedMeshKeeper();

	virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock);

	static MStatus initialize();
	static void* creator();

public:
	static MTypeId id;
	static MString nodeName;

//--------------- attribute ---------------

	static MObject aReset;
	static MObject aInputOriginalMesh;
	static MObject aInputModifedMesh;
	static MObject aOutputMesh;

	static MString nameReset;
	static MString nameInputOriginalMesh;
	static MString nameInputModifiedMesh;
	static MString nameOutputMesh;

private:
	MPointArray mem_pointsResult;
	MObject     mem_oOutputMesh;
};