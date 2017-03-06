#include "volumeSurfaceCenterCurve.h"
#include "volumeSurfaceCenterCurve_def.h"


MTypeId     volumeSurfaceCenterCurve::id( 0xc8d301 );

MObject    volumeSurfaceCenterCurve::aInputSurface;

MObject    volumeSurfaceCenterCurve::aOutputCurve;

volumeSurfaceCenterCurve::volumeSurfaceCenterCurve() 
{
	centerCrvKnots.setLength( 0 );
}
volumeSurfaceCenterCurve::~volumeSurfaceCenterCurve() 
{
}

void* volumeSurfaceCenterCurve::creator()
{
	return new volumeSurfaceCenterCurve();
}

MStatus volumeSurfaceCenterCurve::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hInputSurface = data.inputValue( aInputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnNurbsSurface fnSurface = hInputSurface.asNurbsSurface();
	getSurfaceInfo( fnSurface );

	MPointArray centerPoints;
	getCenterCurvePoints( fnSurface, centerPoints, status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnNurbsCurve fnCurve;
	MFnNurbsCurveData curveData;
	MObject curveObject = curveData.create();
	
	fnCurve.create( centerPoints, centerCrvKnots, degreeU, MFnNurbsCurve::kOpen, 0,0, curveObject );

	MDataHandle hOutputCurve = data.outputValue( aOutputCurve, &status );
	hOutputCurve.set( curveObject );

	MFnNurbsCurve fnCreateCurve( curveObject );

	data.setClean( plug );

	return MS::kSuccess;
}