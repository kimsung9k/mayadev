#ifndef _sgHair_fixCurvePointOnMatrix
#define _sgHair_fixCurvePointOnMatrix

#include <maya/MPxNode.h>
#include <maya/MTypeId.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>


class sgHair_fixCurvePointOnMatrix : MPxNode
{
public:
	            sgHair_fixCurvePointOnMatrix();
	virtual    ~sgHair_fixCurvePointOnMatrix();


	virtual   MStatus    compute( const MPlug& plug, MDataBlock& data );

	static    void*      creator();
	static    MStatus    initialize();


public:

	static   MTypeId    id;

	static   MObject     aBaseMatrix;

	static   MObject     aInputCurve;
	
	static   MObject     aConstStart;
	static   MObject     aConstEnd;

	static   MObject     aConstPoint;
		static   MObject     aConstPointX;
		static   MObject     aConstPointY;
		static   MObject     aConstPointZ;

	static   MObject     aOutputCurve;
};

#endif