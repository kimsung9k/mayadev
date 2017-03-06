//
// Copyright (C) Locus
// 
// File: volumeCurvesOnSurfaceNode.cpp
//
// Dependency Graph Node: volumeCurvesOnSurface
//
// Author: Maya Plug-in Wizard 2.0
//

#include "volumeCurvesOnSurface.h"
#include "volumeCurvesOnSurface_class.h"

#define SAFE_DELETE(x) if(x) { delete x; x=0; }


MTypeId     volumeCurvesOnSurface::id( 0xc8d302 );

MObject    volumeCurvesOnSurface::aInputSurface;
MObject    volumeCurvesOnSurface::aInputMatrix;
MObject    volumeCurvesOnSurface::aDirection;

MObject    volumeCurvesOnSurface::aByUV;
	
MObject    volumeCurvesOnSurface::aNumOfSample;

MObject    volumeCurvesOnSurface::aCutting;
	MObject    volumeCurvesOnSurface::aCutAble;
	MObject    volumeCurvesOnSurface::aInputMesh;
	MObject    volumeCurvesOnSurface::aMeshMatrix;
	MObject    volumeCurvesOnSurface::aConstStart;
	MObject    volumeCurvesOnSurface::aConstEnd;
	MObject    volumeCurvesOnSurface::aRefresh;

MObject    volumeCurvesOnSurface::aCurveInfo;
	MObject    volumeCurvesOnSurface::aParamRate;
	MObject    volumeCurvesOnSurface::aCenterRate;
	MObject    volumeCurvesOnSurface::aStartEP;
		MObject    volumeCurvesOnSurface::aStartEPx;
		MObject    volumeCurvesOnSurface::aStartEPy;
		MObject    volumeCurvesOnSurface::aStartEPz;
	MObject    volumeCurvesOnSurface::aStartIndex;
	MObject    volumeCurvesOnSurface::aPolygonIndex;
	MObject    volumeCurvesOnSurface::aUValue;
	MObject    volumeCurvesOnSurface::aVValue;
	MObject    volumeCurvesOnSurface::aCutParam;

MObject    volumeCurvesOnSurface::aOutputCurve;

volumeCurvesOnSurface::volumeCurvesOnSurface() 
{
	centerCrvKnots.setLength( 0 );
}
volumeCurvesOnSurface::~volumeCurvesOnSurface() 
{
}

void* volumeCurvesOnSurface::creator()
{
	return new volumeCurvesOnSurface();
}

MStatus volumeCurvesOnSurface::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;
	
	//MFnDependencyNode thisNode( thisMObject() );
	//cout << thisNode.name() << ", volumeCurvesOnSurface" << endl;

	if( plug != aOutputCurve  )
		return MS::kSuccess;

	MDataHandle hInputSurface = data.inputValue( aInputSurface, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputMatrix  = data.inputValue( aInputMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hNumOfSample  = data.inputValue( aNumOfSample, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hByUV         = data.inputValue( aByUV, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	byUV = hByUV.asBool();

	MArrayDataHandle hArrCurveInfo = data.inputArrayValue( aCurveInfo, &status );
	MMatrix inputMatrix = hInputMatrix.asMatrix();

	int elementNum = hArrCurveInfo.elementCount();
	int numSample = hNumOfSample.asInt();

	MObject surfaceObj = hInputSurface.asNurbsSurface();;

	MFnNurbsSurface *pFnSurface = new MFnNurbsSurface( surfaceObj );
	getSurfaceInfo( *pFnSurface, status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	CenterCurve centerCurveInst( pFnSurface, numCVsU, numCVsV, degreeU, &centerCrvKnots );
	centerCurveInst.getCenterPointsAndParam( numSpansU+1, minRangeU, maxRangeU );

	MPointArray centerCrvPoints = centerCurveInst.outCenterPoints;
	MDoubleArray paramUArr = centerCurveInst.outParamArr;

	MArrayDataHandle hArrOutputCurve = data.outputArrayValue( aOutputCurve );
	MArrayDataBuilder bOutputCurve( aOutputCurve, elementNum, &status );

	MDataHandle hCutting    = data.inputValue( aCutting );
	MDataHandle hInputMesh  = hCutting.child( aInputMesh );
	MDataHandle hMeshMatrix = hCutting.child( aMeshMatrix );
	MDataHandle hConstStart = hCutting.child( aConstStart );
	MDataHandle hBlendArea  = hCutting.child( aConstEnd );
	MDataHandle hCutAble    = hCutting.child( aCutAble );
	MDataHandle hRefresh    = hCutting.child( aRefresh );

	double paramU;
	double paramV;
	double centerRate;
	MPoint surfPoint;
	MObjectArray crvObjects;
	crvObjects.setLength( elementNum );
	MPointArray createPoints;
	createPoints.setLength( numSpansU+1 );

	MFnNurbsCurve fnCreateCurve;

	for( int i=0; i< elementNum; i++ )
	{
		MDataHandle hCurveInfo = hArrCurveInfo.inputValue();

		paramV  = hCurveInfo.child( aParamRate ).asDouble();
		centerRate = hCurveInfo.child( aCenterRate ).asDouble();

		for( int j=0; j<numSpansU+1; j++ )
		{
			paramU = paramUArr[j];
			pFnSurface->getPointAtParam( paramU, paramV, surfPoint );
			MPoint& centerCrvPoint = centerCrvPoints[j];

			createPoints[j] = centerCrvPoint*(1-centerRate) + surfPoint*centerRate;
			createPoints[j] *= inputMatrix;
		}
		MFnNurbsCurveData crvData;
		crvObjects[i] = crvData.create();
		fnCreateCurve.createWithEditPoints( createPoints, degreeU, MFnNurbsCurve::kOpen, 0,0,0, crvObjects[i], &status );
		if( !status )
		{
			MFnDependencyNode thisNode( thisMObject() );
			cout << thisNode.name() << endl;
			CHECK_MSTATUS_AND_RETURN_IT( status );
		}
		hArrCurveInfo.next();
	}

	bool   refresh    = hRefresh.asBool();

	if( refresh )
	{
		MDagPath inputMeshDagPath;
		MObject oInputMesh = hInputMesh.asMesh();
		MMatrix meshMatrix = hMeshMatrix.asMatrix();
		CHECK_MSTATUS_AND_RETURN_IT( status );

		int elementNum = hArrCurveInfo.elementCount();

		MMeshIntersector intersector;
		intersector.create( oInputMesh, meshMatrix );

		MFnMesh fnMesh( oInputMesh );
		MPointOnMesh pointOnMesh;
		for( int i=0; i<elementNum; i++ )
		{
			hArrCurveInfo.jumpToElement( i );

			MFnNurbsCurve fnCurve( crvObjects[i] );
			double cutParam = getCloestParamOnMesh( fnCurve, oInputMesh, meshMatrix );

			MPoint closePoint;
			fnCurve.getPointAtParam( cutParam, closePoint );

			intersector.getClosestPoint( closePoint, pointOnMesh );
			int closeFaceIndex = pointOnMesh.faceIndex();

			MMatrix matrix = getMatrixByPolygonIndex( inputMeshDagPath, oInputMesh, closeFaceIndex )*meshMatrix;

			MDataHandle hCurveInfo = hArrCurveInfo.inputValue();
			
			float2 uvValue;
			uvValue[0] = -1.0f;
			uvValue[1] = -1.0f;

			if( byUV )
			{
				fnMesh.getUVAtPoint( closePoint*meshMatrix.inverse(), uvValue );
				fnMesh.getPointAtUV( closeFaceIndex, closePoint, uvValue );

				matrix( 3,0 ) = closePoint.x;
				matrix( 3,1 ) = closePoint.y;
				matrix( 3,2 ) = closePoint.z;
			}

			MDataHandle hUValue  = hCurveInfo.child( aUValue );
			MDataHandle hVValue  = hCurveInfo.child( aVValue );
			hUValue.setFloat( uvValue[0] );
			hVValue.setFloat( uvValue[1] );

			int getStartIndex;
			MPointArray startEP = getCurrentCurvePoints( fnCurve, cutParam, fnCurve.length(), matrix.inverse(), MDoubleArray(), getStartIndex );

			MArrayDataHandle hArrStartEP = hCurveInfo.child( aStartEP );
			MDataHandle hPolygonIndex = hCurveInfo.child( aPolygonIndex );
			MDataHandle hCutParam = hCurveInfo.child( aCutParam );
			MDataHandle hStartIndex = hCurveInfo.child( aStartIndex );
			hStartIndex.set( getStartIndex );
			
			MArrayDataBuilder bArrStartEP( aStartEP, startEP.length(), &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );

			for( int j=0; j<startEP.length(); j++ )
			{
				MDataHandle hStartEP = bArrStartEP.addElement( j );
				hStartEP.set( MVector( startEP[j] ) );
			}/**/
			hPolygonIndex.setInt( closeFaceIndex );
			hCutParam.setDouble( cutParam );

			hArrStartEP.set( bArrStartEP );
			hArrStartEP.setAllClean();
		}

		hRefresh.setBool( false );
	}

	if( !hCutAble.asBool() )
	{
		for( int i=0; i< elementNum; i++ )
		{
			hArrCurveInfo.jumpToElement( i );
			MDataHandle hOutputCurve = bOutputCurve.addElement( hArrCurveInfo.elementIndex() );
			hOutputCurve.set( crvObjects[i] );
		}
	}
	else
	{
		double constStart = hConstStart.asDouble();
		double constEnd   = hBlendArea.asDouble();
		if( constEnd < constStart )
		{
			constEnd = constStart+0.1;
		}

		MDagPath inputMeshDagPath;
		MObject oInputMesh = hInputMesh.asMesh();
		MMatrix meshMatrix = hMeshMatrix.asMatrix();
		MFnMesh fnMesh = oInputMesh;

		if( oInputMesh == MObject::kNullObj )
		{
			for( int i=0; i< elementNum; i++ )
			{
				hArrCurveInfo.jumpToElement( i );
				MDataHandle hOutputCurve = bOutputCurve.addElement( hArrCurveInfo.elementIndex() );
				hOutputCurve.set( crvObjects[i] );
			}
		}
		else
		{
			MFnNurbsCurve createCutCurve;
			MFnNurbsCurveData cutCurveData;
			MObject cutCurveObj = cutCurveData.create();

			for( int i=0; i<elementNum; i++ )
			{
				MFnNurbsCurve fnCurve( crvObjects[i] );
				hArrCurveInfo.jumpToElement( i );
				MDataHandle hCurveInfo = hArrCurveInfo.inputValue();

				MArrayDataHandle hArrStartEP = hCurveInfo.child( aStartEP );
				MDataHandle hPolygonIndex    = hCurveInfo.child( aPolygonIndex );
				MDataHandle hUValue         = hCurveInfo.child( aUValue );
				MDataHandle hVValue         = hCurveInfo.child( aVValue );
				MDataHandle hCutParam        = hCurveInfo.child( aCutParam );

				double curveLength = fnCurve.length();

				int currentSpans = fnCurve.numSpans();
				double cutParam = hCutParam.asDouble();

				int handleCVCount = hArrStartEP.elementCount();

				if( currentSpans > handleCVCount )
				{
					hArrCurveInfo.jumpToElement( i );
					MDataHandle hOutputCurve = bOutputCurve.addElement( hArrCurveInfo.elementIndex() );
					hOutputCurve.set( crvObjects[i] );
				}
				else
				{
					hArrCurveInfo.jumpToElement( i );

					MFnNurbsCurve currentCurve( crvObjects[i] );
					int polygonIndex = hPolygonIndex.asInt();
					float2 uvValue;
					uvValue[0] = hUValue.asFloat();
					uvValue[1] = hVValue.asFloat();
					double cutParam  = hCutParam.asDouble();
					MMatrix faceMatrix  = getMatrixByPolygonIndex( inputMeshDagPath, oInputMesh, polygonIndex )*meshMatrix;
				
					if( byUV && uvValue[0] != -1.0f && uvValue[1] != -1.0f )
					{
						MPoint closePoint;
						fnMesh.getPointAtUV( polygonIndex, closePoint, uvValue );
						closePoint*= meshMatrix;

						faceMatrix( 3,0 ) = closePoint.x;
						faceMatrix( 3,1 ) = closePoint.y;
						faceMatrix( 3,2 ) = closePoint.z;
					}

					MPointArray startPoints   = getStartCurvePoints( hArrStartEP );
					MDoubleArray params;
					int dumyGetIndex;
					MDataHandle hStartIndex = hArrCurveInfo.inputValue().child( aStartIndex );
					MPointArray currentPoints = getCurrentCurvePoints( currentCurve, cutParam, curveLength, faceMatrix.inverse(), params, dumyGetIndex, hStartIndex.asInt() );
					MPointArray blendPoints = getBlendPoints( constStart, constEnd, &startPoints, &currentPoints, faceMatrix, params );
					
					createCutCurve.createWithEditPoints( blendPoints, degreeU, MFnNurbsCurve::kOpen, 0,0,0, cutCurveObj, &status );
					CHECK_MSTATUS_AND_RETURN_IT( status );
					MDataHandle hOutputCurve = bOutputCurve.addElement( hArrCurveInfo.elementIndex() );
					hOutputCurve.set( cutCurveObj );
				}
			}
			crvObjects.clear();
		}
	}

	hArrOutputCurve.set( bOutputCurve );
	hArrOutputCurve.setAllClean();

	data.setClean( plug );

	delete pFnSurface;

	//cout << thisNode.name() << ", volumeCurvesOnSurface end" << endl;

	return MS::kSuccess;
}

MStatus volumeCurvesOnSurface::initialize()	
{
	MStatus				stat;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute  mAttr;
	MFnTypedAttribute   tAttr;
	MFnCompoundAttribute cAttr;

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
 	tAttr.setArray( true );
	tAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aOutputCurve ) );

	aByUV = nAttr.create( "byUv", "byUv", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aByUV ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aByUV, aOutputCurve ) );

	aInputSurface = tAttr.create( "inputSurface", "inputSurface", MFnData::kNurbsSurface );
	tAttr.setStorable( true );
	tAttr.setCached( false );
	CHECK_MSTATUS( addAttribute( aInputSurface ) );
	CHECK_MSTATUS( attributeAffects( aInputSurface, aOutputCurve ) );

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	CHECK_MSTATUS( addAttribute( aInputMatrix ) );
	CHECK_MSTATUS( attributeAffects( aInputMatrix, aOutputCurve ) );

	aNumOfSample = nAttr.create( "numOfSample", "numOfSample", MFnNumericData::kInt, 20 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	nAttr.setMin( 2 );
	CHECK_MSTATUS( addAttribute( aNumOfSample ) );
	CHECK_MSTATUS( attributeAffects( aNumOfSample, aOutputCurve ) );

	aCutting    = cAttr.create( "cutting", "cutting" );
	aCutAble    = nAttr.create( "cutAble", "cutAble", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	aInputMesh  = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	tAttr.setStorable( false );
	tAttr.setCached( false );
	aMeshMatrix  = mAttr.create( "meshMatrix", "meshMatrix" );
	mAttr.setStorable( false );
	aConstStart = nAttr.create( "constStart", "constStart", MFnNumericData::kDouble, 0.0 );
	nAttr.setMin( 0.0 );
	nAttr.setKeyable( true );
	nAttr.setStorable( true );
	aConstEnd  = nAttr.create( "constEnd", "constEnd", MFnNumericData::kDouble, 0.1 );
	nAttr.setMin( 0.01 );
	nAttr.setKeyable( true );
	nAttr.setStorable( true );
	aRefresh    = nAttr.create( "refresh", "refresh", MFnNumericData::kBoolean, false );
	cAttr.addChild( aCutAble );
	cAttr.addChild( aInputMesh );
	cAttr.addChild( aMeshMatrix );
	cAttr.addChild( aConstStart );
	cAttr.addChild( aConstEnd );
	cAttr.addChild( aRefresh );

	CHECK_MSTATUS( addAttribute( aCutting ) );
	CHECK_MSTATUS( attributeAffects( aCutting, aOutputCurve ) );

	aCurveInfo   = cAttr.create( "curveInfo", "curveInfo" );
	aParamRate   = nAttr.create( "paramRate", "paramRate", MFnNumericData::kDouble, 0.0 );
	aCenterRate  = nAttr.create( "centerRate", "centerRate", MFnNumericData::kDouble, 0.75 );
	aStartEPx = nAttr.create( "startEPx", "startEPx", MFnNumericData::kDouble, 0.0 );
	aStartEPy = nAttr.create( "startEPy", "startEPy", MFnNumericData::kDouble, 0.0 );
	aStartEPz = nAttr.create( "startEPz", "startEPz", MFnNumericData::kDouble, 0.0 );
	aStartEP  = nAttr.create( "startEP", "startEP", aStartEPx, aStartEPy, aStartEPz );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	aStartIndex   = nAttr.create( "startIndex", "startIndex", MFnNumericData::kInt, 0 );
	aPolygonIndex = nAttr.create( "polygonIndex", "polygonIndex", MFnNumericData::kInt, 0 );
	aUValue      = nAttr.create( "uValue", "uValue", MFnNumericData::kFloat, -1.0f );
	aVValue      = nAttr.create( "vValue", "vValue", MFnNumericData::kFloat, -1.0f );
	aCutParam     = nAttr.create( "cutParam", "cutParam", MFnNumericData::kDouble, 0.0 );
	cAttr.addChild( aParamRate );
	cAttr.addChild( aCenterRate );
	cAttr.addChild( aStartIndex );
	cAttr.addChild( aStartEP );
	cAttr.addChild( aPolygonIndex );
	cAttr.addChild( aUValue );
	cAttr.addChild( aVValue );
	cAttr.addChild( aCutParam );
	cAttr.setArray( true );
	cAttr.setUsesArrayDataBuilder( true );
	cAttr.setStorable( true );

	CHECK_MSTATUS( addAttribute( aCurveInfo ) );
	CHECK_MSTATUS( attributeAffects( aCurveInfo, aOutputCurve ) );

	return MS::kSuccess;
}