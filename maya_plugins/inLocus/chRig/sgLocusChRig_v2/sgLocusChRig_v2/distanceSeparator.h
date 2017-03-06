#ifndef _distanceSeparator_h
#define _distanceSeparator_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>

class distanceSeparator : public MPxNode
{
public:
						distanceSeparator();
	virtual				~distanceSeparator(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aInputDistance;
	static  MObject     aMultMinus;

	static  MObject     aParameter;
	static  MObject     aSepDistance;

	static	MTypeId		id;
};

#endif