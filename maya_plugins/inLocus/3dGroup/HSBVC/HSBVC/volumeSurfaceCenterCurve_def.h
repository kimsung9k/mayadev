#ifndef _volumeSurfaceCenterCurve_def_h
#define _volumeSurfaceCenterCurve_def_h

#include "volumeSurfaceCenterCurve.h"

MDoubleArray volumeSurfaceCenterCurve::buildKnots( int numCVs, int degree )
{
	int pointLength = numCVs+degree-1;
	MDoubleArray knots;
	knots.setLength( pointLength );
	
	double maxKnot = numCVs - degree;

	double knot;
	for( int i = 0; i< knots.length(); i++ )
	{
		knot = i - degree + 1;
		
		if( knot <= 0 )
			knot = 0;
		else if( knot >= maxKnot )
			knot = maxKnot;

		knots[i] = knot;
	}
	return knots;
}

void volumeSurfaceCenterCurve::getSurfaceInfo( MFnNurbsSurface& fnSurface )
{
	int cuDegreeU = fnSurface.degreeU();
	int cuDegreeV = fnSurface.degreeV();
	int cuFormU = fnSurface.formInU();
	int cuFormV = fnSurface.formInV();
	int cuNumCVsU = fnSurface.numCVsInU();
	int cuNumCVsV = fnSurface.numCVsInV();

	bool different = false;
	
	if( degreeU != cuDegreeU ){ 
		degreeU = cuDegreeU;
		different = true; 
	}
	if( degreeV != cuDegreeV ){ 
		degreeV = cuDegreeV;
		different = true; 
	}
	if( formU != cuFormU ){ 
		formU = cuFormU;
		different = true; 
	}
	if( formV != cuFormV ){ 
		formV = cuFormV;
		different = true; 
	}
	if( numCVsU != cuNumCVsU ){ 
		numCVsU = cuNumCVsU;
		different = true; 
	}
	if( numCVsV != cuNumCVsV ){ 
		numCVsV = cuNumCVsV;
		different = true; 
	}

	if( different )
	{
		centerCrvKnots = buildKnots( numCVsU, degreeU );
	}
}

void volumeSurfaceCenterCurve::getCenterCurvePoints( MFnNurbsSurface& fnSurface, MPointArray& centerPoints, MStatus& status )
{
	centerPoints.setLength( numCVsU );

	MPoint surfPoint;
	for( int i=0; i< numCVsU; i++ )
	{
		MBoundingBox boundingBox;
		for( int j=0; j< numCVsV; j++ )
		{
			fnSurface.getCV( i, j, surfPoint );
			boundingBox.expand( surfPoint );
		}
		centerPoints[i] = ( ( boundingBox.min() + boundingBox.max() )/2.0 );
	}
}

MStatus volumeSurfaceCenterCurve::initialize()	
{
	MStatus				stat;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute  mAttr;
	MFnTypedAttribute   tAttr;

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS( addAttribute( aOutputCurve ) );

	aInputSurface = tAttr.create( "inputSurface", "inputSurface", MFnData::kNurbsSurface );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputSurface ) );
	CHECK_MSTATUS( attributeAffects( aInputSurface, aOutputCurve ) );

	return MS::kSuccess;
}

#endif