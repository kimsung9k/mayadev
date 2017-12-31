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
#include <maya/MFnMeshData.h>

#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MMatrixArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <vector>

#include "sgMeshInfo.h"


class sgFootPrintMesh : public MPxDeformerNode
{
public:
	sgFootPrintMesh();
	virtual ~sgFootPrintMesh();

	virtual MStatus deform(MDataBlock& data, MItGeometry& iter, const MMatrix& mtxGeo, unsigned int multiIndex);
	void deformEach( const sgMeshInfo& meshInfo, MPointArray& points, MMatrix deformerMatrix);

	MStatus setDependentsDirty(const MPlug& plug, MPlugArray& plugArr);
	static MStatus initialize();
	static void* creator();

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

	static MObject aInputs;
		static MObject aMesh;
		static MObject aMatrix;

//----------attribute names--------------

	static MString nameInputs;
		static MString nameMesh;
		static MString nameMatrix;

private:
	std::vector< bool >     mem_dirtyList;
	std::vector< bool >     mem_connectedList;
	std::vector<sgMeshInfo> mem_inputMeshInfos;

	MObject mem_meshOrig;
	MObject mem_modifiedMesh;
};