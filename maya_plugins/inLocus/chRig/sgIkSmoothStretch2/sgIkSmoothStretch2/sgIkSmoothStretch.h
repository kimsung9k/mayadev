#ifndef _sgIkSmoothStretch_h
#define _sgIkSmoothStretch_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

class sgIkSmoothStretch : public MPxNode
{
public:
						sgIkSmoothStretch();
	virtual				~sgIkSmoothStretch();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aInputDistance;
	static  MObject		aInPosition;
		static  MObject     aInPositionX;
		static  MObject     aInPositionY;
		static  MObject     aInPositionZ;

	static  MObject     aSmoothArea;

	static  MObject     aOutputDistance;
	static  MObject     aStretchAble;

	static	MTypeId		id;
};

#endif