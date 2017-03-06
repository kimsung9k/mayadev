#ifndef _sgSeparate_h
#define _sgSeparate_h


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

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/MArrayDataBuilder.h>

#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include "sgBuildMeshData.h"
#include <vector>

#include <maya/MThreadPool.h>


#define NUM_THREAD  48


struct sgSeparate_TaskData 
{
    vector<MPointArray>* m_pPointArraysInput;
	MMatrixArray*        m_pMtxArrInput;
	sgBuildMeshData_array* m_pMeshDataArray_input;
	sgBuildMeshData_array* m_pMeshDataArray_output;
    float envelope;
};


struct sgSeparate_ThreadData
{
    unsigned int start;
    unsigned int end;
    unsigned int numThread;
    sgSeparate_TaskData* pTask;
};



using namespace std;




class sgSeparate: public MPxNode
{
public:
	sgSeparate();
	virtual ~sgSeparate();

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void* creator();
	static  MStatus initialize();

	MStatus separateEachElement( MObject oMesh, int index );
	void    getGrowSelection( MObject oMesh, 
		const sgPolygonPerVertex_array& polygonsPerVetices,
		int startIndex, MIntArray& idsVertex, MIntArray& checkedVertices );


	MStatus                setThread();
	MStatus                endThread();
	static  void           parallelCompute_build( void* data, MThreadRootTask *pRoot );
	static  MThreadRetVal  threadCompute_build( void* pThread );

	static  void           parallelCompute_setPosition( void* data, MThreadRootTask *pRoot );
	static  MThreadRetVal  threadCompute_setPosition( void* pThread );

	static  MTypeId id;

	static  MObject  aInputMeshs;
	static  MObject  aElements;
		static  MObject  aElementIndices;
	static  MObject  aOutputMeshs;

private:

	MIntArray  m_numVertices_inputs;
	MIntArray  m_numPolygons_inputs;
	bool  m_require_update;

	bool  m_isDirty_inputMesh;
	bool  m_isDirty_element;
	int   m_elementNum;

	MFnMesh m_fnInputMesh;

	sgBuildMeshData_array m_meshDataArray;
	sgBuildMeshData_array m_meshDataArray_output;

	MObjectArray m_oArrMeshs;

	sgSeparate_ThreadData* m_pThread;
	sgSeparate_TaskData*   m_pTask;
};


#endif