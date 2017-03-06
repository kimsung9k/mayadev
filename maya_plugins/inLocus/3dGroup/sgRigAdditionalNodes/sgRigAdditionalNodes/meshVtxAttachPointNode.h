#ifndef _meshVtxAttachPointNode_h
#define _meshVtxAttachPointNode_h


#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MTypeId.h>
#include <maya/MItGeometry.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnMesh.h>
#include <maya/MMatrix.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MGlobal.h>


class PointDirtyInfo
{
	unsigned int m_logicalIndex;
	MIntArray    m_indicesVtx;

	PointDirtyInfo& operator=( const PointDirtyInfo& other )
	{
		m_logicalIndex = other.m_logicalIndex;
	}
};


class PointDirtyInfoArray
{
	PointDirtyInfoArray::PointDirtyInfoArray()
	{
		m_pPointDirtyInfo = new PointDirtyInfo[0];
	}

	PointDirtyInfoArray::~PointDirtyInfoArray()
	{
		delete []m_pPointDirtyInfo;
	}

	void setLength( unsigned int length )
	{
		PointDirtyInfo* pPointDirtyInfo = new PointDirtyInfo[ length ];

		for( unsigned int i; i< this->length; i++ )
		{
			pPointDirtyInfo[i] = m_pPointDirtyInfo[i];
		}

		delete []m_pPointDirtyInfo;
		m_pPointDirtyInfo = pPointDirtyInfo;
		this->length = length;
	}

	unsigned int length;
	PointDirtyInfo*  m_pPointDirtyInfo;
}


class MeshVtxAttachPointNode : public MPxNode
{
public:
						MeshVtxAttachPointNode();
	virtual				~MeshVtxAttachPointNode();
	
	virtual MStatus     compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MTypeId     id;

	static  MObject		aOutPoint;
		static  MObject		aOutPointX;
		static  MObject		aOutPointY;
		static  MObject		aOutPointZ;

	static  MObject     aBaseMesh;
	static  MObject		aPointInfo;
		static  MObject		aVtxIndex;
		static  MObject     aNormalDistance;
		static  MObject		aMultWidthBBS; // BBS == bounding box size

private:
	MIntArray m_indicesPointInfoDirty;
};


#endif