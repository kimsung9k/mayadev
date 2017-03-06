#ifndef _sgSlidingDeformer_h
#define _sgSlidingDeformer_h


#include <maya/MPxDeformerNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
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


struct sgSlidingDeformerTask
{
	float env;
	MMeshIntersector* pMeshIntersector;
	MPointArray*      pPointsMoved;
	MPointArray*      pPointsBase;
	MIntArray*        pIndicesMoved;
};


struct sgSlidingDeformerThread
{
	int numThread;
	int start;
	int end;
	sgSlidingDeformerTask* pTask;
};


class sgSlidingDeformer : public MPxDeformerNode
{
public:
						sgSlidingDeformer();
	virtual				~sgSlidingDeformer();
	
	virtual MStatus     deform( MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int index );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MStatus checkDeformedVertices( const MPointArray& basePoints, const MPointArray& movedPoints, 
		                           MIntArray& movedIndices );

	MStatus computeSliding();

	void    setThread();
	void    endThread();
	static	void	parallelCompute( void* data, MThreadRootTask *pRoot );
	static	MThreadRetVal	deformCompute( void* pThread );

	void check_time_start();
	void check_time_end( float& a, bool& b );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aSlidingBaseMesh;
	static  MObject     aMoveMesh;
	static	MTypeId		id;
	
public:
	bool m_isSlidingBaseDirty;
	bool m_isMoveMeshDirty;
	bool m_isOrigMeshDirty;

	MMeshIntersector* m_pMeshIntersector;
	MFnMesh     m_meshSlidingBase;
	MFnMesh     m_meshMove;
	MPointArray m_pointsBase;
	MPointArray m_pointsMoved;
	MIntArray   m_indicesMoved;

	sgSlidingDeformerTask*		    m_pTask;
	sgSlidingDeformerThread*		m_pThread;
	unsigned int                    m_numThread;

public:
	__int64 m_freq, m_start, m_end; 
	BOOL m_condition;
};


#endif