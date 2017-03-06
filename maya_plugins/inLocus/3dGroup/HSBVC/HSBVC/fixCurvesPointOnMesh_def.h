#include "fixCurvesPointOnMesh.h"

MPointArray fixCurvesPointOnMesh::getVtxPoints( MFnMesh& fnMesh, int polygonIndex )
{
	MIntArray vertexNums; 
	fnMesh.getPolygonVertices( polygonIndex, vertexNums );
	MPointArray vtxPoints;
	vtxPoints.setLength( 3 );
	fnMesh.getPoint( vertexNums[0], vtxPoints[0] );
	fnMesh.getPoint( vertexNums[1], vtxPoints[1] );
	fnMesh.getPoint( vertexNums[2], vtxPoints[2] );
	return vtxPoints;
}


MMatrix  fixCurvesPointOnMesh::getMatrixByPolygonIndex( MFnMesh& fnMesh, int polygonIndex )
{
	MPointArray vtxPoints = getVtxPoints( fnMesh, polygonIndex );

	MPoint yPoint = vtxPoints[0];
	MPoint cPoint = vtxPoints[1];
	MPoint xPoint = vtxPoints[2];

	MVector yVector = yPoint - cPoint;
	MVector xVector = xPoint - cPoint;
	
	double avDist = ( yVector.length() + xVector.length() )/ 2.0;

	MVector zVector = ( xVector^yVector ).normal() * avDist;

	double buildMatrix[4][4] = { xVector.x, xVector.y, xVector.z, 0,
		                         yVector.x, yVector.y, yVector.z, 0,
						         zVector.x, zVector.y, zVector.z, 0,
						         cPoint.x , cPoint.y,  cPoint.z,  1 };

	return MMatrix( buildMatrix );
}


int fixCurvesPointOnMesh::getClosestFaceIndex( MFnMesh& mesh, MPoint point )
{
	int numPolygon = mesh.numPolygons();

	MIntArray vtxIndies;
	MPointArray vtxPoints;
	mesh.getPoints( vtxPoints );

	int closestIndex = 0;
	double closestLength = 10000;
	double sumLength;

	for( int i=0; i< numPolygon; i++ )
	{
		mesh.getPolygonVertices( i, vtxIndies );
		
		int indexLength = vtxIndies.length();

		MVector sumPoint( 0,0,0 );

		for( int j=0; j< indexLength; j++ )
		{
			sumPoint += vtxPoints[ vtxIndies[j] ];
		}
		sumPoint /= indexLength;

		sumLength = ( sumPoint - point ).length();

		if( sumLength < closestLength )
		{
			closestLength = sumLength;
			closestIndex = i;
		}
	}
	return closestIndex;
}


MStatus   fixCurvesPointOnMesh::curveInfoToTesk( MArrayDataHandle& hArrCurveInfo, taskData* pTask, MFnMesh& fnMesh, bool refresh, MIntArray& curveInfoIndies )
{
	MStatus status;

	MObject* pCurveObj;

	MFnDependencyNode thisNode = thisMObject();
	MPlug curveInfoPlug = thisNode.findPlug( aCurveInfo );

	if( refresh )
	{
		int curveInfoLength = curveInfoPlug.numElements();

		pCurveObj = new MObject[ curveInfoLength ];

		for( int i=0; i< curveInfoLength; i++ )
		{
			MPlug curveInfoElementPlug = curveInfoPlug[i];
			curveInfoIndies[i] = curveInfoElementPlug.logicalIndex();

			MPlug startMatrixPlug = curveInfoElementPlug.child( aStartMatrix );
			MPlug startCVPlug     = curveInfoElementPlug.child( aStartCV );
			MPlug polygonIndexPlug= curveInfoElementPlug.child( aPolygonIndex );
			MPlug moveCurvePlug   = curveInfoElementPlug.child( aMoveCurve );
			
			MPlugArray connections;
			moveCurvePlug.connectedTo( connections, true, false );

			MObject crvObject;
			if( connections.length() )
				crvObject = connections[0].node();
			else
				crvObject = moveCurvePlug.asMObject();
			pCurveObj[i] = crvObject;

			MFnNurbsCurve fnMoveCurve( crvObject );
			MPointArray movePoints;
			fnMoveCurve.getCVs( movePoints );
			int pointLength = movePoints.length();
			int degree = fnMoveCurve.degree();
			if( pointLength == 0 )
			{
				movePoints.setLength( 4 );
				pointLength = 4;
				degree = 3;
			}
			int closeFaceIndex = getClosestFaceIndex( fnMesh, movePoints[0] );
			
			MMatrix faceMatrix = getMatrixByPolygonIndex( fnMesh, closeFaceIndex );
			MPointArray startPoints;
			startPoints.setLength( pointLength);
			for( int j=0; j<pointLength; j++ )
			{
				startPoints[j] = movePoints[j]*faceMatrix.inverse();
			}
			MFnMatrixData matData;
			matData.create( faceMatrix );
			startMatrixPlug.setMObject( matData.object() );
			polygonIndexPlug.setInt( closeFaceIndex );
			for( int j=0; j<pointLength; j++ )
			{
				MPlug startCVElementPlug = startCVPlug.elementByLogicalIndex( j );
				startCVElementPlug.child( 0 ).setDouble( startPoints[j].x );
				startCVElementPlug.child( 1 ).setDouble( startPoints[j].y );
				startCVElementPlug.child( 2 ).setDouble( startPoints[j].z );
			}
			pTask->pDegrees[i] = degree;
			pTask->pStartCurvePoints[i] = startPoints;
			pTask->pVtxPoints[i]        = getVtxPoints( fnMesh, closeFaceIndex );
			pTask->pMovedCurvePoints[i] = movePoints;
		}
	}
	else
	{
		int elementNum = hArrCurveInfo.elementCount();

		pCurveObj = new MObject[ elementNum ];

		for( int i=0; i< elementNum; i++ )
		{
			hArrCurveInfo.jumpToElement( i );
			curveInfoIndies[i] = hArrCurveInfo.elementIndex();

			MDataHandle hCurveInfo = hArrCurveInfo.inputValue( &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );

			MDataHandle      hStartMatrix  = hCurveInfo.child( aStartMatrix );
			MArrayDataHandle   hArrStartCV = hCurveInfo.child( aStartCV );
			MDataHandle      hPolygonIndex = hCurveInfo.child( aPolygonIndex );
			MDataHandle      hMoveCurve    = hCurveInfo.child( aMoveCurve );

			MFnNurbsCurve    fnMoveCurve   = hMoveCurve.asNurbsCurve();

			MPlug curveInfoElementPlug = curveInfoPlug[i];

			MPlug moveCurvePlug   = curveInfoElementPlug.child( aMoveCurve );
			
			MPlugArray connections;
			moveCurvePlug.connectedTo( connections, true, false );

			MObject crvObject;
			if( connections.length() )
				crvObject = connections[0].node();
			else
				crvObject = moveCurvePlug.asMObject();
			pCurveObj[i] = crvObject;

			MPointArray movePoints;
			fnMoveCurve.getCVs( movePoints );

			int moveCVElementNum = movePoints.length();

			MPointArray startPoints;
			startPoints.setLength( moveCVElementNum );
			for( int j=0; j<moveCVElementNum; j++ )
			{
				startPoints[j] = hArrStartCV.inputValue().asVector();
				hArrStartCV.next();
			}
			pTask->pDegrees[i] = fnMoveCurve.degree();
			pTask->pStartCurvePoints[i] = startPoints;
			pTask->pVtxPoints[i] = getVtxPoints( fnMesh, hPolygonIndex.asInt() );
			pTask->pMovedCurvePoints[i] = movePoints;
		}
	}

	pTask->pCurveObj = pCurveObj;

	return MS::kSuccess;
}


MStatus  fixCurvesPointOnMesh::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	tAttr.setArray( true );
	tAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aOutputCurve ) );

	aBaseMesh = tAttr.create( "baseMesh", "baseMesh", MFnData::kMesh );
	tAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aBaseMesh ) );
	CHECK_MSTATUS( attributeAffects( aBaseMesh, aOutputCurve ) );

	aConstStart = nAttr.create( "constStart", "constStart", MFnNumericData::kFloat, 0.0f );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aConstStart ) );
	CHECK_MSTATUS( attributeAffects( aConstStart, aOutputCurve ) );

	aBlendArea  = nAttr.create( "blendArea", "blendArea", MFnNumericData::kFloat, 1.0f );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aBlendArea ) );
	CHECK_MSTATUS( attributeAffects( aBlendArea, aOutputCurve ) );

	aRefresh   = nAttr.create( "refresh", "refresh", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aRefresh ) );
	CHECK_MSTATUS( attributeAffects( aRefresh, aOutputCurve ) );

	aCurveInfo = cAttr.create( "curveInfo", "curveInfo" );

	aStartMatrix = mAttr.create("startMatrix","startMatrix" );
	aStartCVx = nAttr.create( "startCVx", "startCVx", MFnNumericData::kDouble, 0.0 );
	aStartCVy = nAttr.create( "startCVy", "startCVy", MFnNumericData::kDouble, 0.0 );
	aStartCVz = nAttr.create( "startCVz", "startCVz", MFnNumericData::kDouble, 0.0 );
	aStartCV  = nAttr.create( "startCV", "startCV", aStartCVx, aStartCVy, aStartCVz );
	nAttr.setArray( true );
	aPolygonIndex = nAttr.create( "polygonIndex", "polygonIndex", MFnNumericData::kInt, 0 );
	aMoveCurve = tAttr.create( "moveCurve", "moveCurve", MFnData::kNurbsCurve );

	cAttr.addChild( aStartMatrix );
	cAttr.addChild( aStartCV );
	cAttr.addChild( aPolygonIndex );
	cAttr.addChild( aMoveCurve );
	cAttr.setStorable( true );
	cAttr.setArray( true );

	CHECK_MSTATUS( addAttribute( aCurveInfo ) );
	CHECK_MSTATUS( attributeAffects( aCurveInfo, aOutputCurve ) );

	return MS::kSuccess;
}