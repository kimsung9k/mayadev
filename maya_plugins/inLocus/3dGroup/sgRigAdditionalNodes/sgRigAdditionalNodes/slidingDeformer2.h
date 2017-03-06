#ifndef _slidingDeformer2_h
#define _slidingDeformer2_h


#include <maya/MPxDeformerNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MItGeometry.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnMesh.h>
#include <maya/MMatrix.h>

#include <maya/MMeshIntersector.h>

#include <maya/MFnMesh.h>

#include <maya/MGlobal.h>
#include <Windows.h>

#include <maya/MThreadPool.h>



class MIntDoubleArray
{
public:
	int length;
	MIntArray* pIntArr;
public:
	MIntDoubleArray() : length(0)
	{
		pIntArr = new MIntArray[0];
	}
	void setLength( int inputLength )
	{
		MIntArray* pIntArrNew = new MIntArray[inputLength];
		int copyLength;
		if( this->length > inputLength )
			copyLength = inputLength;
		else
			copyLength = this->length;

		for( int i=0; i< copyLength; i++ )
		{
			pIntArrNew[i] = this->pIntArr[i];
		}
		delete[] this->pIntArr;
		this->pIntArr = pIntArrNew;
		this->length = inputLength;
	}
	int size()
	{
		return this->length;
	}
	MIntArray& operator[]( unsigned int index )
	{
		return this->pIntArr[ index ];
	}
	~MIntDoubleArray()
	{
		delete []this->pIntArr;
	}
};



struct slidingDeformer2ChkIndicesTask
{
	MPointArray* pPointsOrig;
	MPointArray* pPointsMoved;
	MIntArray*   pIndicesMoved;
	MIntDoubleArray IndicesThread;
};



struct slidingDeformer2ChkIndicesThread
{
	int numThread;
	int start;
	int end;
	int threadIndex;
	slidingDeformer2ChkIndicesTask* pTask;
};



struct slidingDeformer2GetDistTask
{
	MMeshIntersector* pMeshIntersector;
	MPointArray*      pPointsOrig;
	MVectorArray*     pVectors;
};



struct slidingDeformer2GetDistThread
{
	int numThread;
	int start;
	int end;
	slidingDeformer2GetDistTask* pTask;
};



struct slidingDeformer2SlidingTask
{
	float             env;
	MMeshIntersector* pMeshIntersector;
	MPointArray*      pPointsMoved;
	MPointArray*      pPointsResult;
	MVectorArray*     pVectorArr;
	MIntArray*        pIndicesCheck;
};



struct slidingDeformer2SlidingThread
{
	int numThread;
	int start;
	int end;
	slidingDeformer2SlidingTask* pTask;
};



class slidingDeformer2 : public MPxDeformerNode
{
public:
						slidingDeformer2();
	virtual				~slidingDeformer2();
	
	virtual MStatus     deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int index );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	void    setThread_getDist();
	void    endThread_getDist();
	static	void	parallelCompute_getDist( void* data, MThreadRootTask *pRoot );
	static	MThreadRetVal	compute_getDist( void* pThread );

	MStatus getSlidingDistance();

	void    setThread_chkIndices();
	void    endThread_chkIndices();
	static	void	parallelCompute_chkIndices( void* data, MThreadRootTask *pRoot );
	static	MThreadRetVal	compute_chkIndices( void* pThread );

	MStatus checkDeformedVertices();
	MStatus checkDeformedVertices( const MPointArray& basePoints, const MPointArray& movedPoints, 
		                           MIntArray& movedIndices );

	void    setThread_sliding();
	void    endThread_sliding();
	static	void	parallelCompute_sliding( void* data, MThreadRootTask *pRoot );
	static	MThreadRetVal	compute_sliding( void* pThread );

	MStatus sliding();

	void check_time_start();
	void check_time_end( float& a, bool& b );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aBaseMesh;
	static  MObject     aOrigMesh;
	static  MObject     aCheckAllPoints;
	static  MObject     aCheckTime;
	static	MTypeId		id;
	
public:
	bool m_isBaseMeshDirty;
	bool m_isOrigMeshDirty;
	bool m_isInputGeomDirty;

	float m_env;

	MMeshIntersector* m_pMeshIntersector;
	MPointArray  m_pointsOrig;
	MPointArray  m_pointsMoved;
	MPointArray  m_pointsResult;
	MVectorArray m_vectorArr;
	MIntArray*   m_pIndicesCheck;
	MIntArray    m_indicesMoved;
	MIntArray    m_indicesAllPoints;

	bool m_checkAllPoints;

	slidingDeformer2GetDistTask*		m_pTaskGetDist;
	slidingDeformer2GetDistThread*		m_pThreadGetDist;
	slidingDeformer2ChkIndicesTask*     m_pTaskChkIndices;
	slidingDeformer2ChkIndicesThread*   m_pThreadChkIndices;
	slidingDeformer2SlidingTask*		m_pTaskSliding;
	slidingDeformer2SlidingThread*		m_pThreadSliding;
	unsigned int                m_numThread;

public:
	__int64 m_freq, m_start, m_end; 
	BOOL m_condition;
};


#endif