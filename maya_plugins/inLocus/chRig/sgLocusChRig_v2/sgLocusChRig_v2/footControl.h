#ifndef _footControl_h
#define _footControl_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MTypeId.h>

class footControl : public MPxNode
{
public:
						footControl();
	virtual				~footControl(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aFootStart;
	static  MObject     aFootEnd;

	static  MObject     aWalkRollAngle;

	static  MObject     aHeelRot;
	static  MObject     aBallRot;
	static  MObject     aToeRot;
	static  MObject     aHeelTwist;
	static  MObject     aBallTwist;
	static  MObject     aToeTwist;
	static  MObject     aBank;
	static  MObject     aTapToe;
	static  MObject     aHeelLift;
	static  MObject     aWalkRoll;

	static  MObject     aOutput;

	static	MTypeId		id;
};

#endif