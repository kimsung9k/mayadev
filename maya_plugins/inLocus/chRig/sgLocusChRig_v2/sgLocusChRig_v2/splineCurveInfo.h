#ifndef _splineCurveInfo_h
#define _splineCurveInfo_h

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h>

class splineCurveInfo : public MPxNode
{
public:
						splineCurveInfo();
	virtual				~splineCurveInfo(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aInputCurve;
	static  MObject     aTurnOnPercentage;
	static  MObject     aParamFromLength;

	static  MObject     aStartTransform;
	static  MObject     aEndTransform;

	static  MObject     aStartUpAxis;
	static  MObject     aEndUpAxis;

	static  MObject     aTargetAimAxis;
	static  MObject     aTargetUpAxis;

	static  MObject  aParameter;

	static  MObject     aOutput;
		static  MObject     aDistance;
		static  MObject     aBetweenDistance;

		static  MObject     aRotateByTangent;

		static  MObject     aPosition;
			static  MObject     aPositionX;
			static  MObject     aPositionY;
			static  MObject     aPositionZ;
		static  MObject     aRotate;
			static  MObject     aRotateX;
			static  MObject     aRotateY;
			static  MObject     aRotateZ;

	static	MTypeId		id;
};

#endif