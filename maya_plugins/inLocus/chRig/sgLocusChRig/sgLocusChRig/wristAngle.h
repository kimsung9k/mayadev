#ifndef _wristAngleNode
#define _wristAngleNode

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

 
class wristAngle : public MPxNode
{
public:
						wristAngle();
	virtual				~wristAngle(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     inputAxis;
	static  MObject		inputMatrix;
	static  MObject     angleRate;
	static  MObject		outAngle;

	static	MTypeId		id;
};

#endif
