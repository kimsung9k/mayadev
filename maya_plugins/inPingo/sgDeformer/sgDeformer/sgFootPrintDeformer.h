#pragma once


#include <maya/MFnMesh.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MItGeometry.h>
#include <maya/MPlugArray.h>
#include <maya/MTypeId.h>

#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MBoundingBox.h>

#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MMatrixArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <vector>

#include "sgMeshInfo.h"


class sgFootPrintDeformer : public MPxNode
{
public:
	sgFootPrintDeformer();
	virtual ~sgFootPrintDeformer();

	virtual MStatus compute(const MPlug& plug, MDataBlock& data);

	MStatus setDependentsDirty(const MPlug& plug, MPlugArray& plugArr);
	static MStatus initialize();
	static void* creator();

	void restoreDeformMesh();

	void restoreElementList();
	void restoreMeshs( unsigned int index );
	void restoreMatrices( unsigned int index );
	void setDirty( unsigned int index );
	void finalize();

	MObject getThisGeometryObject();

public:
	static MTypeId id;
	static MString deformerName;

//----------attribute--------------
	static MObject aInputMesh;
	static MObject aInputMeshMatrix;

	static MObject aInputs;
		static MObject aMesh;
		static MObject aMatrix;

	static MObject aOutputMesh;

//----------attribute names--------------
	static MString nameInputMesh;
	static MString nameInputMeshMatrix;

	static MString nameInputs;
		static MString nameMesh;
		static MString nameMatrix;

	static MString nameOutputMesh;

private:
	std::vector< bool >    mem_dirtyList;
	std::vector< bool >    mem_connectedList;
	std::vector<sgMeshInfo> mem_inputMeshInfos;

	MObject mem_modifiedMesh;
};