#ifndef _slidingDeformer_h
#define _slidingDeformer_h


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


struct slidingDeformerTask
{
	MMeshIntersector* pMeshIntersector;
	MPointArray*      pPointsMoved;
	MIntArray*        pIndicesMoved;
};


struct slidingDeformerThread
{
	int numThread;
	int start;
	int end;
	slidingDeformerTask* pTask;
};


class slidingDeformer : public MPxDeformerNode
{
public:
						slidingDeformer();
	virtual				~slidingDeformer();
	
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
	static  MObject     aBaseMesh;
	static	MTypeId		id;
	
public:
	bool m_isBaseMeshDirty;
	bool m_isOrigMeshDirty;

	MMeshIntersector* m_pMeshIntersector;
	MFnMesh     m_meshBase;
	MPointArray m_pointsBase;
	MPointArray m_pointsMoved;
	MIntArray   m_indicesMoved;

	slidingDeformerTask*		m_pTask;
	slidingDeformerThread*		m_pThread;
	unsigned int                m_numThread;

public:
	__int64 m_freq, m_start, m_end; 
	BOOL m_condition;
};


#endif