#include "clusterControledSurface.h"
#include "clusterControledSurface_def.h"
//#include "clusterControledSurface_threadDef.h"

MTypeId   clusterControledSurface::id( 0xc8d305 );

MObject   clusterControledSurface::aInputOrigCurve;
MObject   clusterControledSurface::aInputOrigCurveMatrix;
MObject   clusterControledSurface::aInputCurve;
MObject   clusterControledSurface::aInputCurveMatrix;
MObject   clusterControledSurface::aInputSurface;
MObject   clusterControledSurface::aInputSurfaceMatrix;

MObject   clusterControledSurface::aBaseUpMatrix;
MObject   clusterControledSurface::aUpMatrix;

MObject   clusterControledSurface::aUpMatrixChangeAble;

MObject   clusterControledSurface::aCheckPoint;
//MObject   clusterControledSurface::aNumTasks;

MObject   clusterControledSurface::aOutputSurface;

clusterControledSurface::clusterControledSurface()
{
	//MThreadPool::init();
	inOrigCurve   = MObject();
	inSurface     = MObject();
	inBaseUpMatrix = MMatrixArray();
	baseUpMatrixChanged = false;
}
clusterControledSurface::~clusterControledSurface()
{
	//MThreadPool::release();
}

void* clusterControledSurface::creator()
{
	return new clusterControledSurface();
}

MStatus   clusterControledSurface::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hInputOrigCurve = data.inputValue( aInputOrigCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputOrigCurveMatrix = data.inputValue( aInputOrigCurveMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputCurve = data.inputValue( aInputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputCurveMatrix = data.inputValue( aInputCurveMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputSurface = data.inputValue( aInputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputSurfaceMatrix = data.inputValue( aInputSurfaceMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MArrayDataHandle hArrBaseUpMatrix = data.inputArrayValue( aBaseUpMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MArrayDataHandle hArrUpMatrix = data.inputArrayValue( aUpMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hUpMatrixChange  = data.inputValue( aUpMatrixChangeAble, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hCheckPoint  = data.inputValue( aCheckPoint, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	//MDataHandle hNumTasks    = data.inputValue( aNumTasks, &status );
	//CHECK_MSTATUS_AND_RETURN_IT( status );
	//int numTasks = hNumTasks.asInt();

	MObject oInputSurface = hInputSurface.asNurbsSurface();
	MObject oInputOrigCurve = hInputOrigCurve.asNurbsCurve();
	MObject oInputCurve = hInputCurve.asNurbsCurve();
	MMatrix mtxSurface = hInputSurfaceMatrix.asMatrix();
	MMatrix mtxOrigCurve = hInputOrigCurveMatrix.asMatrix();
	MMatrix mtxCurve = hInputCurveMatrix.asMatrix();
	bool  checkPoint = hCheckPoint.asBool();
	upMatrixChangeAble = hUpMatrixChange.asBool();

	status = updateBaseUpMatrix( oInputOrigCurve, mtxOrigCurve, hArrUpMatrix, hArrBaseUpMatrix, checkPoint );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = updateInputSurfaceInfo( oInputOrigCurve, oInputSurface, mtxOrigCurve, mtxSurface, checkPoint );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnNurbsSurfaceData fnSurfaceData;
	MObject oOutputSurface = fnSurfaceData.create();
	MFnNurbsSurface  fnCreateSurface;

	fnCreateSurface.copy( oInputSurface, oOutputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = moveSurfacePoints( oInputCurve, oOutputSurface, mtxCurve, mtxSurface, hArrUpMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hOutputSurface = data.outputValue( aOutputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	hOutputSurface.set( oOutputSurface );

	data.setClean( plug );

	return MS::kSuccess;
}

MStatus  clusterControledSurface::initialize()
{
	MStatus  status;

	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MFnTypedAttribute    tAttr;
	MFnCompoundAttribute cAttr;

	aOutputSurface = tAttr.create( "outputSurface", "outputSurface", MFnData::kNurbsSurface );
	CHECK_MSTATUS( addAttribute( aOutputSurface ) );

	aInputOrigCurve = tAttr.create( "inputOrigCurve", "inputOrigCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputOrigCurve ) );
	CHECK_MSTATUS( attributeAffects( aInputOrigCurve, aOutputSurface ) );

	aInputOrigCurveMatrix = mAttr.create( "inputOrigCurveMatrix", "inputOrigCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputOrigCurveMatrix ) );
	CHECK_MSTATUS( attributeAffects( aInputOrigCurveMatrix, aOutputSurface ) );

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurve ) );
	CHECK_MSTATUS( attributeAffects( aInputCurve, aOutputSurface ) );

	aInputCurveMatrix = mAttr.create( "inputCurveMatrix", "inputCurveMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputCurveMatrix ) );
	CHECK_MSTATUS( attributeAffects( aInputCurveMatrix, aOutputSurface ) );

	aInputSurface = tAttr.create( "inputSurface", "inputSurface", MFnData::kNurbsSurface );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputSurface ) );
	CHECK_MSTATUS( attributeAffects( aInputSurface, aOutputSurface ) );

	aInputSurfaceMatrix = mAttr.create( "inputSurfaceMatrix", "inputSurfaceMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInputSurfaceMatrix ) );
	CHECK_MSTATUS( attributeAffects( aInputSurfaceMatrix, aOutputSurface ) );

	aBaseUpMatrix = mAttr.create( "baseUpMatrix", "baseUpMatrix" );
	mAttr.setStorable( true );
	mAttr.setArray( true );
	mAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aBaseUpMatrix ) );
	CHECK_MSTATUS( attributeAffects( aBaseUpMatrix, aOutputSurface ) );

	aUpMatrix = mAttr.create( "upMatrix", "upMatrix" );
	mAttr.setStorable( true );
	mAttr.setArray( true );
	CHECK_MSTATUS( addAttribute( aUpMatrix ) );
	CHECK_MSTATUS( attributeAffects( aUpMatrix, aOutputSurface ) );

	aUpMatrixChangeAble = nAttr.create( "upMatrixChangeAble", "upMatrixChangeAble", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aUpMatrixChangeAble ) );
	CHECK_MSTATUS( attributeAffects( aUpMatrixChangeAble, aOutputSurface ) );

	aCheckPoint = nAttr.create( "checkPoint", "checkPoint", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aCheckPoint ) );
	CHECK_MSTATUS( attributeAffects( aCheckPoint, aOutputSurface ) );
	/*
	aNumTasks = nAttr.create( "numTasks" , "numTasks", MFnNumericData::kInt, 32 );
	nAttr.setStorable( true );
	nAttr.setKeyable( false );
	nAttr.setChannelBox( true );
	CHECK_MSTATUS( addAttribute( aNumTasks ) );
	*/

	return MS::kSuccess;
}