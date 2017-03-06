#ifndef _blendAndFixedShape_h
#define _blendAndFixedShape_h

#include <maya/MPxDeformerNode.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MObjectArray.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMessageAttribute.h>

#include <maya/MItGeometry.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MFnAnimCurve.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include <maya/MTypeId.h> 

#include <maya/MGlobal.h>

#include <maya/MThreadPool.h>

#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>

#include <maya/MFloatArray.h>

#include <vector>

#define  NUM_THREAD  32;

using namespace std;

struct  blendAndFixedShape_taskData
{
	MFloatArray blendMeshWeights;
	MObjectArray oArrAnimCurve;
	MFloatArray largeOverValues;
	MIntArray weightedIndices;

	MPointArray   basePoints;
	int deltaLength;
	vector< MPointArray > deltas;
	vector< MPointArray > weightedDeltas;
	MPointArray   movedPoints;
};

struct  blendAndFixedShape_threadData
{
	int  numThread;
	int  start;
	int  end;
	blendAndFixedShape_taskData* pTaskData;
};


class blendAndFixedShape : public MPxDeformerNode
{
public:
						blendAndFixedShape();
	virtual				~blendAndFixedShape();

	virtual MStatus     deform( MDataBlock& data,
                                MItGeometry& itGeo,
                                const MMatrix& localToWorldMatrix,
                                unsigned int geomIndex );
	void    finishCaculation();

	virtual MStatus		setDependentsDirty( const MPlug& dirtyPlug, MPlugArray& affectedPlugs );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus		meshPoints_To_DeltaAttrs( MArrayDataHandle& hArrBlendMeshInfos );
	MStatus		deltaAttrs_To_Task( MArrayDataHandle& hArrBlendMeshInfos );
	MStatus     reOrdereDeltas( MArrayDataHandle& hArrBlendMeshInfos );

	MStatus     currentWeights_To_task( MArrayDataHandle& hArrDriverWeights ); 
	void		weightAttrs_To_task( MArrayDataHandle& hArrBlendMeshInfos );

	float       getWeightFromWeights( MFloatArray& weights, MFloatArray& targetWeights );

	void        getBlendMeshWeight();
	void        setOverIndicesArray( MArrayDataHandle& hArrBlendMeshInfos );
	void        setOverWeights();
	void        setEnvWeights();

	void        separateSameChannelIndices();
	void        shareWeightBySameChannel();
	void        setWeightedBlendIndices();

	MStatus     setBlendMeshWeightByAnimCurve();

	static  MStatus        setPoints();
	static  void           parallelCompute( void* data, MThreadRootTask *pRoot );
	static  MThreadRetVal  deformCompute( void* pThread );

	void    setThread();
	void    endThread();

public:
	static  MObject     aDriverWeights;
	static  MObject     aMinusWeightEnable;

	static  MObject     aBlendMeshInfos;
		static  MObject     aInputMesh;
		static  MObject     aDeltas;
			static  MObject     aDeltaX;
			static  MObject     aDeltaY;
			static  MObject     aDeltaZ;
		static  MObject     aTargetWeights;
		static	MObject		aMeshName;
		static  MObject		aKeepMatrix;
		static  MObject     aAnimCurve;
		static  MObject     aAnimCurveOutput;

	static  MObject     aUpdateMeshData;

	static	MTypeId		id;

public:
	bool        blendMeshUpdated;
	float envValue;

	int createMirrorIndex;

	int beforeBlendMeshNum;
	blendAndFixedShape_taskData*   pTaskData;
	blendAndFixedShape_threadData* pThreadData;

	MIntArray  updateBlendMeshIndices;
	MIntArray  updateDeltaIndices;

	MFloatArray driverWeights;
	vector< MIntArray > targetIndicesArray;
	vector< MFloatArray > targetWeightsArray;
	vector< MIntArray > overIndicesArray;

	vector< MIntArray > sameChannelIndicesArray;
};

#endif