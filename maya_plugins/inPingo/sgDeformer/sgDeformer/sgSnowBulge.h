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

#include <maya/MItMeshVertex.h>

#include <maya/MMatrix.h>
#include <maya/MQuaternion.h>

#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MSelectionList.h>
#include <maya/MPlugArray.h>
#include <maya/MDagPath.h>

class sgSnowBulge : public MPxNode
{
public:
	sgSnowBulge();
	virtual ~sgSnowBulge();

	virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock);

	static MStatus initialize();
	static void* creator();

	void getModifiedPoints( MPointArray &resultPoints, 
		const MPointArray& pointsModified, const MPointArray& pointsOriginal, 
		MIntArray* ptrModifiedIndicesMap =NULL );
	void getBulgePoints(MPointArray &resultPoints,
		const MFloatVectorArray& normalOrig, const MFloatVectorArray& normalModified,
		const MIntArray& mapModified, MItMeshVertex& itVtx, 
		float weightBulge, float radiusBulge);

public:
	static MTypeId id;
	static MString nodeName;

	//--------------- attribute ----------------
	static MObject aReset;
	static MObject aBulgeWeight;
	static MObject aBulgeRadius;
	static MObject aInputOriginalMesh;
	static MObject aInputModifedMesh;
	static MObject aOutputMesh;

	static MString nameReset;
	static MString nameBulgeWeight;
	static MString nameBulgeRadius;
	static MString nameInputOriginalMesh;
	static MString nameInputModifiedMesh;
	static MString nameOutputMesh;
	//-------------------------------------------

private:
	MIntArray   mem_modifiedKeepIndicesMap;

	MPointArray mem_pointsOrig;;
	MPointArray mem_pointsModifiedKeep;
	MPointArray mem_pointsResult;

	MObject     mem_oMeshModifiedKeep;
	MObject     mem_oMeshResult;
};