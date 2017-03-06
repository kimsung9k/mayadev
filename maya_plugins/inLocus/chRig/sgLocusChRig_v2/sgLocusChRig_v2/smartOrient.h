#ifndef _smartOrientNode
#define _smartOrientNode

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MTypeId.h> 

 
class smartOrient : public MPxNode
{
public:
						smartOrient();
	virtual				~smartOrient(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     aimAxis;
	static  MObject		inputMatrix;
	static  MObject     outputMatrix;
	static  MObject     outAngle;
		static  MObject		outAngleX;		
		static  MObject		outAngleY;
		static  MObject		outAngleZ;
	static  MObject     aAngleRateFirst;
	static  MObject     aAngleRateSecond;
	static  MObject     aAngleRateThird;

	static	MTypeId		id;
};

#endif
