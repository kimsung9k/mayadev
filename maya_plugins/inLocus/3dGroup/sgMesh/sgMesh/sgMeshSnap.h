#ifndef _sgMeshSnap_h
#define _sgMeshSnap_h


#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MObject.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MItGeometry.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MFnMesh.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MPxDeformerNode.h>


class sgMeshSnap : public MPxDeformerNode
{
public:
					    sgMeshSnap();
	virtual 		    ~sgMeshSnap();
	virtual MStatus     deform( MDataBlock &data, MItGeometry &itGeo, const MMatrix &localToWorldMatrix, unsigned int mIndex );
	virtual MStatus     setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );
	static  void*	    creator();
	static  MStatus     initialize();

	static  MTypeId		id;
    static  MObject		aSnapMesh;
    static  MObject		aIdsMap;

public:
	bool m_isDirtyIdsMap;

	MPointArray m_pointsSnap;
	MIntArray   m_indicesSnapVerticesMap;
};

#endif
