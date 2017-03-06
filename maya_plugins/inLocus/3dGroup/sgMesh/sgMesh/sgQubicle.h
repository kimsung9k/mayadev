#ifndef _sgQubicle_h
#define _sgQubicle_h


#include <maya/MPxNode.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MTypeId.h>
#include <maya/MStatus.h>
#include <maya/MSyntax.h>
#include <maya/MPlugArray.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MMeshIntersector.h>

#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>
#include <maya/MBoundingBox.h>
#include <vector>

#include <maya/MThreadPool.h>


#define NUM_THREAD  48

using namespace std;

class sgQubicle: public MPxNode
{
public:
	sgQubicle();
	virtual ~sgQubicle();

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void* creator();
	static  MStatus initialize();

	static  MTypeId id;

	static  MObject  aInputMesh;
	static  MObject  aInputMeshMatrix;
	static  MObject  aPointDetail;
	static  MObject  aOutputMesh;
};


#endif