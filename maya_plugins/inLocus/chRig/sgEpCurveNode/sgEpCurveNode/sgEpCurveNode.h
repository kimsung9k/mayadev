#ifndef _sgEpCurveNode_h
#define _sgEpCurveNode_h


#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h> 


class sgEpCurveNode : public MPxNode
{
public:
						sgEpCurveNode();
	virtual				~sgEpCurveNode(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject     aInputPoint;
		static  MObject   aInputPointX;
		static  MObject   aInputPointY;
		static  MObject   aInputPointZ;
	static  MObject     aDegree;
	static  MObject		aOutputCurve;

	static	MTypeId		id;
};

#endif
