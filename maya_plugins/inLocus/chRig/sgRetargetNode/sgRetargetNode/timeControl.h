#ifndef _timeControl_h
#define _timeControl_h


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTypeId.h> 

 
class timeControl : public MPxNode
{
public:
						timeControl();
	virtual				~timeControl(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		aInTime;

	static  MObject     aWeight;
	static  MObject     aOffset;
	static  MObject     aMult;

	static  MObject     aLimitAble;
	static  MObject     aMinTime;
	static  MObject     aMaxTime;

	static  MObject     aOutTime;
	static  MObject     aOutWeight;

	static	MTypeId		id;

};

#endif
