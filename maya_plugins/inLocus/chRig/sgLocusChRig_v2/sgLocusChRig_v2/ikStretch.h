#ifndef _ikstretch_h
#define _ikstretch_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

class ikStretch : public MPxNode
{
public:
						ikStretch();
	virtual				~ikStretch(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     aInputDistance;
	static  MObject		aInPosition;
		static  MObject     aInPositionX;
		static  MObject     aInPositionY;
		static  MObject     aInPositionZ;
	static  MObject     aOutputDistance;
	static  MObject     aStretchAble;

	static	MTypeId		id;
};

#endif