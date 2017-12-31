#pragma once

#include <maya/MPxDeformerNode.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MTypeId.h>
#include <maya/MDataHandle.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>

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
#include <maya/MItGeometry.h>
#include <vector>

#include "sgMeshInfo.h"

class sgBulgeDeformer : public MPxDeformerNode
{
public:
	sgBulgeDeformer();
	virtual ~sgBulgeDeformer();

	virtual MStatus deform(MDataBlock& block, MItGeometry& iter, const MMatrix& mtx, unsigned int index);

	virtual MStatus setDependentsDirty(const MPlug& plug, MPlugArray& plugs);

	static MStatus initialize();
	static void* creator();

public:
	static MTypeId id;
	static MString nodeName;

	//--------------- attribute ----------------
	static MObject aBulgeWeight;
	static MObject aBulgeRadius;
	static MObject aBulgeInputs;
		static MObject aMatrix;
		static MObject aMesh;
	
	static MString nameBulgeWeight;
	static MString nameBulgeRadius;
	static MString nameBulgeInputs;
		static MString nameMatrix;
		static MString nameMesh;
	//-------------------------------------------

private:
	std::vector<sgMeshInfo*> mem_meshInfosInner;
	std::vector<sgMeshInfo*> mem_meshInfosOuter;

	unsigned int mem_maxLogicalIndex;
	bool mem_resetElements;
};