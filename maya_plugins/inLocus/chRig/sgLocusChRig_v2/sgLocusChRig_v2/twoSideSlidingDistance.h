#ifndef _twoSideSlidingDistance_h
#define _twoSideSlidingDistance_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h> 

class twoSideSlidingDistance : public MPxNode
{
public:
						twoSideSlidingDistance();
	virtual				~twoSideSlidingDistance(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     aInputDistance1;
	static  MObject     aInputDistance2;
	static  MObject     aSliding;
	static  MObject     aDistance;
	static  MObject     aOutputDistance1;
	static  MObject     aOutputDistance2;
	
	static  MObject     aSlidingAttrSize;
	static  MObject     aDistanceAttrSize;

	static	MTypeId		id;
};

#endif