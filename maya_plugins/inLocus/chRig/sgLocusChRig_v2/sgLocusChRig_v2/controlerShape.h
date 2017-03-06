#ifndef _controlerShape_h
#define _controlerShape_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MTypeId.h>

class controlerShape : public MPxNode
{
public:
						controlerShape();
	virtual				~controlerShape(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aControlerType;

	static  MObject     aOffset;
		static  MObject     aOffsetX;
		static  MObject     aOffsetY;
		static  MObject     aOffsetZ;
	static  MObject     aOrient;
		static  MObject     aOrientX;
		static  MObject     aOrientY;
		static  MObject     aOrientZ;
	static  MObject     aSize;
		static  MObject     aSizeX;
		static  MObject     aSizeY;
		static  MObject     aSizeZ;

	static  MObject     aOutputCurve;

	static	MTypeId		id;
};

#endif