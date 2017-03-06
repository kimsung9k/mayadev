#ifndef _sgSkinClsuter_h
#define _sgSkinCluster_h


#include <maya/MFnMesh.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MItGeometry.h>
#include <maya/MTypeId.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MMatrixArray.h>

class sgSkinCluster : public MPxDeformerNode
{
public:
	sgSkinCluster();
	virtual ~sgSkinCluster();

	virtual MStatus deform( MDataBlock& block, MItGeometry &iter, const MMatrix& mat, unsigned int multiIndex );
	
	static MStatus initialize();
	static void* creator();

	static MTypeId id;

	static MObject aMatrix;
	static MObject aBindPreMatrix;
	static MObject aGeomMatrix;

	MFnDependencyNode m_fnThisNode;
	MPlug m_plugMatrix;
	unsigned int m_logicalLength;

	MMatrixArray m_mtxForMult;
	MMatrixArray m_mtxMatrix;
	MMatrixArray m_mtxBindPre;
};



#endif