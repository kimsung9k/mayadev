#include "simulatedCurveControledSurface.h"
#include "simulatedCurveControledSurface_def.h"

MTypeId  simulatedCurveControledSurface::id( 0xc8d307 );

MObject  simulatedCurveControledSurface::aBaseUpMatrix;
MObject  simulatedCurveControledSurface::aMoveUpMatrix;
MObject  simulatedCurveControledSurface::aBaseSurfaceMatrix;
MObject  simulatedCurveControledSurface::aScaleMatrix;
MObject  simulatedCurveControledSurface::aBaseSurface;
MObject  simulatedCurveControledSurface::aBaseCurve;
MObject  simulatedCurveControledSurface::aCurrentTime;
MObject  simulatedCurveControledSurface::aMoveCurve;

MObject  simulatedCurveControledSurface::aOutputSurface;

void*  simulatedCurveControledSurface::creator()
{
	return new simulatedCurveControledSurface();
}

simulatedCurveControledSurface::simulatedCurveControledSurface()
{
	requireUpdateSurface = true;
	requireUpdateCurve = true;
};

simulatedCurveControledSurface::~simulatedCurveControledSurface()
{
};

MStatus simulatedCurveControledSurface::compute( const MPlug& plug, MDataBlock& data )
{
	//MFnDependencyNode thisNode( thisMObject() );
	//cout << thisNode.name() << ", start" << endl;

	MStatus status;

	MDataHandle  hBaseUpMatrix = data.inputValue( aBaseUpMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hMoveUpMatrix = data.inputValue( aMoveUpMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hBaseSurfaceMatrix = data.inputValue( aBaseSurfaceMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hScaleMatrix = data.inputValue( aScaleMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hBaseSurface = data.inputValue( aBaseSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hBaseCurve  = data.inputValue( aBaseCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hMoveCurve  = data.inputValue( aMoveCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hCurrentTime = data.inputValue( aCurrentTime, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix  baseUpMatrix  =  hBaseUpMatrix.asMatrix();
	MMatrix  moveUpMatrix  =  hMoveUpMatrix.asMatrix();
	MMatrix  baseSurfaceMatrix  = hBaseSurfaceMatrix.asMatrix();
	MMatrix  scaleMatrix   = hScaleMatrix.asMatrix();
	MObject   oBaseSurface = hBaseSurface.asNurbsSurface();
	MObject   oBaseCurve   = hBaseCurve.asNurbsCurve();
	MObject   oMoveCurve   = hMoveCurve.asNurbsCurve();

	MFnNurbsSurface baseSurface = oBaseSurface;
	MFnNurbsCurve   baseCurve   = oBaseCurve;
	MFnNurbsCurve   moveCurve   = oMoveCurve;

	if( oBaseSurface.isNull() || oBaseCurve.isNull() || oMoveCurve.isNull() )
	{
		return MS::kInvalidParameter;
	}

	if( requireUpdateCurve )
	{
		getMatrixArrayFromCurve( baseUpMatrix, baseCurve, baseUpMatrixArr );
	}

	getMatrixArrayFromCurve( moveUpMatrix, moveCurve, moveUpMatrixArr, baseUpMatrixArr.length() );

	if( requireUpdateSurface )
	{
		getLocalPointsFromSurface( baseSurface, baseSurfaceMatrix, 
			                       baseCurve, baseUpMatrixArr, baseLocalPoints, baseParamRanges );
	}

	int paramRangeLength = baseParamRanges.length();
	double minParam = moveCurve.findParamFromLength( 0 );
	double maxParam = moveCurve.findParamFromLength( moveCurve.length() );
	double paramLength = maxParam-minParam;
	double paramValue;

	MPointArray pivPoints;
	MDoubleArray paramList;
	pivPoints.setLength( paramRangeLength );
	paramList.setLength( paramRangeLength );

	for( int i=0; i<baseParamRanges.length(); i++ )
	{
		paramList[i] = baseParamRanges[i]*paramLength+minParam;
		moveCurve.getPointAtParam( paramList[i], pivPoints[i] );
	}

	MPointArray returnPoints;
	
	getSurfaceMovePoints( baseSurfaceMatrix, 
		                  baseLocalPoints, pivPoints, 
						  paramList, 
						  moveUpMatrixArr, 
						  minParam, maxParam, 
						  returnPoints );

	MFnNurbsSurfaceData surfaceData;
	MObject oCopySurface = surfaceData.create();
	baseSurface.copy( oBaseSurface, oCopySurface );

	MFnNurbsSurface copySurface = oCopySurface;
	copySurface.setCVs( returnPoints );

	MDataHandle  hOutputSurface = data.outputValue( aOutputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	hOutputSurface.set( oCopySurface );
	
	data.setClean( plug );

	requireUpdateSurface = false;
	requireUpdateCurve = false;

	//cout << thisNode.name() << ", end" << endl;
	//cout << endl;

	return MS::kSuccess;
}


MStatus  simulatedCurveControledSurface::initialize()
{
	MStatus  status;
	
	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MFnTypedAttribute    tAttr;
	MFnUnitAttribute     uAttr;

	aOutputSurface = tAttr.create( "outputSurface", "outputSurface", MFnData::kNurbsSurface );
	CHECK_MSTATUS( addAttribute( aOutputSurface ) );

	aBaseUpMatrix = mAttr.create( "baseUpMatrix", "baseUpMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aBaseUpMatrix ) );
	CHECK_MSTATUS( attributeAffects( aBaseUpMatrix, aOutputSurface ) );

	aMoveUpMatrix = mAttr.create( "moveUpMatrix", "moveUpMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aMoveUpMatrix ) );
	CHECK_MSTATUS( attributeAffects( aMoveUpMatrix, aOutputSurface ) );

	aBaseSurfaceMatrix = mAttr.create( "baseSurfaceMatrix", "baseSurfaceMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aBaseSurfaceMatrix ) );
	CHECK_MSTATUS( attributeAffects( aBaseSurfaceMatrix, aOutputSurface ) );

	aScaleMatrix = mAttr.create( "scaleMatrix", "scaleMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aScaleMatrix ) );
	CHECK_MSTATUS( attributeAffects( aBaseSurfaceMatrix, aOutputSurface ) );

	aBaseSurface = tAttr.create( "baseSurface", "baseSurface", MFnData::kNurbsSurface );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aBaseSurface ) );
	CHECK_MSTATUS( attributeAffects( aBaseSurface, aOutputSurface ) );

	aBaseCurve = tAttr.create( "baseCurve", "baseCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aBaseCurve ) );
	CHECK_MSTATUS( attributeAffects( aBaseCurve, aOutputSurface ) );

	aMoveCurve = tAttr.create( "moveCurve", "moveCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aMoveCurve ) );
	//CHECK_MSTATUS( attributeAffects( aMoveCurve, aOutputSurface ) );

	aCurrentTime = uAttr.create( "currentTime", "currentTime", MFnUnitAttribute::kTime );
	uAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aCurrentTime ) );
	CHECK_MSTATUS( attributeAffects( aCurrentTime, aOutputSurface ) );

	return MS::kSuccess;
}