#ifndef _inverseSkinCluster_h
#define _inverseSkinCluster_h

#include <maya/MPxDeformerNode.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MObjectArray.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MItGeometry.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>
#include <maya/MFnMatrixData.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MTypeId.h> 

#include <maya/MGlobal.h>

#include <maya/MThreadPool.h>

#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>

#include <vector>

using namespace std;

#define  NUM_THREAD  32;


struct  skinClusterInfo
{
	MMatrixArray matrices;
	MMatrixArray bindPreMatrices;
	MMatrixArray multMatrices;
	vector< MFloatArray > weightsArray;
	vector< MIntArray >   wIndicesArray;
};

struct taskData0
{
	float envelop;
	float invEnv;
	MMatrixArray weightedMatrices;
	MPointArray  basePoints;
	MPointArray  beforePoints;
	MPointArray  afterPoints;
	MPointArray  envPoints;
};

struct threadData0
{
	int numThread;

	int start;
	int end;

	taskData0* pTaskData;
	skinClusterInfo* pSkinInfo;
};

class inverseSkinCluster : public MPxDeformerNode
{
public:
						inverseSkinCluster();
	virtual				~inverseSkinCluster(); 

	virtual MStatus     deform( MDataBlock& data,
                                MItGeometry& itGeo,
                                const MMatrix& localToWorldMatrix,
                                unsigned int geomIndex );
	//virtual MStatus     setDependentsDirty( const MPlug &plug, const MPlugArray& plugArray );

	static  void*		creator();
	static  MStatus		initialize();

	MStatus   updateWeightList();
	MStatus   updateLogicalIndexArray();
	MStatus   updateMatrixAttribute( MArrayDataHandle& hMatrix, MArrayDataHandle& hBindPreMatrix );
	MStatus   updateMatrixInfo( MArrayDataHandle& hMatrix, MArrayDataHandle& hBindPreMatrix );

	void    getWeightedMatrices( MMatrix& geomMatrix );
	MStatus                setThread();
	MStatus                endThread();
	static  void           parallelCompute( void* data, MThreadRootTask *pRoot );
	static  MThreadRetVal  deformCompute( void* pThread );

public:
	static  MObject     aInMesh;
	static  MObject     aGeomMatrix;

	static  MObject     aTargetSkinCluster;
	static  MObject     aUpdateWeightList;

	static  MObject     aMatrix;
	static  MObject     aBindPreMatrix;
	static  MObject     aUpdateMatrix;

	static	MTypeId		id;

public:
	bool weightListUpdated;
	bool matrixAttrUpdated;
	bool matrixInfoUpdated;
	bool originalMeshUpdated;

	MPointArray m_meshPoints;
	MIntArray logicalIndexArray;
	skinClusterInfo* pSkinInfo;
	taskData0* pTaskData;
	threadData0* pThread;
	float envelopValue;

	MIntArray m_logicalMap;
};

#endif