#ifndef _node_h
#define _node_h


#include <maya/MPxDeformerNode.h>
#include <maya/MTypeId.h>
#include <maya/MObject.h>

#include <maya/MFnMessageAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MItGeometry.h>
#include <maya/MItMeshVertex.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>

#include <maya/MPointArray.h>

#include <maya/MFnMesh.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MGlobal.h>

#include <maya/MDagPath.h>

#include "deltaList.h"


class MainNode : public MPxDeformerNode
{
public:
	MainNode();
	virtual ~MainNode();

	static void* creator();
	virtual MStatus deform( MDataBlock& data, MItGeometry& itGeo, const MMatrix& mat, unsigned int multiIndex );
	static MStatus initialize();

	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	MMatrix getMultMtxDelta(  const Weights& weighs );

	MStatus chk_updateSkinClusterInfo( const MMatrix& mtx );
	MStatus chk_inputGeomPoints( const MItGeometry& itMesh );
	MStatus chk_deltaInfoAllUpdate( MArrayDataHandle& hArrDeltaInfo, const MMatrix& mat );
	MStatus chk_deltaInfoMovedUpdate( MArrayDataHandle& hArrDeltaInfo, const MMatrix& mat );
	MStatus chk_updateWeights( MArrayDataHandle& hArrDeltaInfo );
	MStatus caculate();
	

public:
	static  MObject  aMsgSkinCluster;
	static  MObject  aDeltaInfo;
		static  MObject  aDeltaName;
		static  MObject  aInputMesh;
		static  MObject  aDelta;
			static  MObject  aDeltaX;
			static  MObject  aDeltaY;
			static  MObject  aDeltaZ;
		static  MObject  aWeight;

	static  MTypeId  id;

public:
	MPlug         m_plugMtx;
	MPlug         m_plugBindPre;
	MMatrixArray  m_mtxArr;
	MMatrixArray  m_mtxArrBindPre;
	MIntArray     m_intArrMtxLogicalMap;
	DeltaList     m_deltaList;
	MIntArray     m_weightEachShapeLogical;
	MFloatArray   m_weightEachShape;

	bool          m_updateInputGeom;
	MPointArray   m_pointArrBase;
	MPointArray   m_pointArrResult;

	float         m_eachWeight;
	MIntArray     m_indicesUpdateMesh;
	MIntArray     m_weightUpdateIndices;

	unsigned int  m_numDeltaInfo;
	unsigned int  m_numBeforeDeltaInfo;

	MPlug         m_plugDeltaInfo;
	MPlugArray    m_connections;

	MMatrixArray  m_multedMtx;
	MVectorArray  m_addedDeltas;
	MVectorArray  m_defaultDeltas;
};



#endif