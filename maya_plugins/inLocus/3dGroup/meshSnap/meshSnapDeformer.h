#ifndef MESHSNAP_H
#define MESHSNAP_H


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
#include <maya/MPxDeformerNode.h>

#include <iostream>
#include <vector>

class MeshSnap : public MPxDeformerNode
{
public:
					    MeshSnap();
	virtual 		    ~MeshSnap();
	virtual MStatus     deform( MDataBlock &data, MItGeometry &itGeo, const MMatrix &localToWorldMatrix, unsigned int mIndex );
	static  void*	    creator();
	static  MStatus     initialize();

	static  MTypeId		id;
    static  MObject		aSnapMesh;
    static  MObject		aMapping;

};

#endif
