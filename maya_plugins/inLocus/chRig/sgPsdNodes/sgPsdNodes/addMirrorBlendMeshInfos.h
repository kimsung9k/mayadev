#ifndef _addMirrorBlendMeshInfos_h
#define _addMirrorBlendMeshInfos_h

#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>

#include <maya/MItDependencyGraph.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>

#include <maya/MObject.h>
#include <maya/MFnDagNode.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MMatrixArray.h>

#include <maya/M3dView.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include <maya/MGlobal.h>
#include <maya/MDGModifier.h>
#include <maya/MDagModifier.h>

#include <maya/MString.h>

#include <maya/MMeshIntersector.h>

#include <maya/MPxNode.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MThreadPool.h>

#define  ADDMIRROR_NUMTHREAD 1

struct blendMeshInfoData
{
	MString name;

	MIntArray    intArrJoints;
	MMatrixArray mtxArrDefaultJoints;
	MMatrixArray mtxArrTargetJoints;

	MIntArray intArrMirrorTarget;

	MPlug    plugSource;
	MPlug    plugTarget;
};


struct meshIntersectData
{
	MFnMesh  fnMesh;
	MMeshIntersector* p_meshIntersector;

	MIntArray   intArrDeltas;
	MPointArray pointArrDeltas;
};


struct addMirrorThreadData
{
	int numThread;
	int start;
	int end;
	meshIntersectData* pMeshIntersectData;
};


class	addMirrorBlendMeshInfos : public MPxCommand
{
public:
				addMirrorBlendMeshInfos();
	virtual		~addMirrorBlendMeshInfos();

	MStatus		doIt( const MArgList& args );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable()	const;

	static	MSyntax	newSyntax();

	static		void* creator();
	MStatus		getNodes( MDagPath& path);
	MStatus     getJointMatrixInfo();
	MStatus     getMirrorJointIndices();
	MPoint      getPointFromMatrix( MMatrix& mtx );
	MPoint      getMirrorPointFromMatrix( MMatrix& mtx );
	MStatus     getDeltaInfo();

	MStatus     setJointMatrix();
	MMatrix     setMatrixMirror( MMatrix& souceDefault, MMatrix& targetDefault, MMatrix& target );
	MStatus     setDeltas();

	MStatus     createOriginalMesh( MObject& oParent, MObject& oMesh );
	MStatus     connectMeshToTarget( MObject& oMesh );

	static  void           parallelCompute( void* data, MThreadRootTask *pRoot );
	static  MThreadRetVal  deformCompute( void* pThread );
	void setThread();
	void endThread();

public:
	M3dView  m_view;

	MDGModifier m_mdgModifier;
	MDagModifier m_mdagModifier;

	bool   m_bReIntersect;
	static int  m_iVerticesNum;
	static MMeshIntersector* m_pMeshIntersector;

	int  m_iTargetAxisIndex;

	int  m_iSource;
	int  m_iTarget;

	MFnMesh             m_meshTarget;
	MFnDependencyNode   m_fnSkinCluster;
	MFnDependencyNode   m_fnBlendAndFixedShape;

	blendMeshInfoData*   m_pBlendMeshInfoData;
	meshIntersectData*   m_pMeshIntersectData;
	addMirrorThreadData* m_pThreadData;
};

#endif