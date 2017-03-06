#ifndef _volumeSurfaceCenterCurve_h
#define _volumeSurfaceCenterCurve_h

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h> 

#include <maya/MDoubleArray.h>
#include <maya/MPointArray.h>

#include <maya/MPlugArray.h>
#include <maya/MObject.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MPointArray.h>
#include <maya/MBoundingBox.h>

#include <maya/MMatrix.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MGlobal.h>

class volumeSurfaceCenterCurve : public MPxNode
{
public:
						volumeSurfaceCenterCurve();
	virtual				~volumeSurfaceCenterCurve(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();
	
	MDoubleArray buildKnots( int pointLength, int degree );
	void     getSurfaceInfo( MFnNurbsSurface& fnSurface );
	void     getCenterCurvePoints( MFnNurbsSurface& fnSurface, MPointArray& centerPoints, MStatus& status );

public:
	static  MObject     aInputSurface;
	static  MObject		aOutputCurve;

	static	MTypeId		id;

public:
	int numCVsU, numCVsV;
	int degreeU, degreeV;
	int formU, formV;

	MDoubleArray centerCrvKnots;
};

#endif