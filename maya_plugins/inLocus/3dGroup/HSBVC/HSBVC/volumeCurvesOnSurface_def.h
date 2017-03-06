#ifndef _volumeCurvesOnSurface_def_h
#define _volumeCurvesOnSurface_def_h

#include "volumeCurvesOnSurface.h"

void connectToRebuildCurve( MPlug& outputPlug, MPlug& inputPlug, MPlug& cutParamPlug )
{
	MStatus status;

	MDGModifier modify;
	MFnDependencyNode fnNode;
	MObject oNode;

	MPlugArray outputCons;

	outputPlug.connectedTo( outputCons, false, true );

	if( !outputCons.length() )
	{
		MString detachNodeName;

		MGlobal::executeCommand( "createNode detachCurve", detachNodeName, false, false );

		MString connectString = "connectAttr ";
		connectString += outputPlug.name();
		connectString += " ";
		connectString += detachNodeName + ".inputCurve";
		MGlobal::executeCommand( connectString );
	}
}


double getCloseParamOnMesh_detail( MFnNurbsCurve& fnCurve, MFnMesh& fnMesh, double cuParam, double paramRate, MMatrix meshMatrix )
{
	MPoint paramPoint;
	MPoint closePoint;
	MVector closeNormal;
	
	paramRate *= 0.5;
	cuParam += paramRate;
	fnCurve.getPointAtParam( cuParam, paramPoint );
	paramPoint *= meshMatrix.inverse();
	fnMesh.getClosestPointAndNormal( paramPoint, closePoint, closeNormal );
	
	if( paramPoint.distanceTo( closePoint ) < 0.001 || fabs( paramRate ) < 0.0001 )
		return cuParam;

	MVector paramVOnMesh = paramPoint - closePoint;

	double dotValue = paramVOnMesh*closeNormal;

	double result;
	if( dotValue > 0 )
		result = getCloseParamOnMesh_detail( fnCurve, fnMesh, cuParam, -fabs( paramRate ), meshMatrix );
	else
		result = getCloseParamOnMesh_detail( fnCurve, fnMesh, cuParam, fabs( paramRate ), meshMatrix );
	return result;
}


double getCloestParamOnMesh( MFnNurbsCurve& fnCurve, MObject oInputMesh, MMatrix meshMatrix )
{
	int sapNum = 300;

	MFnMesh fnMesh( oInputMesh );
	double maxParam = fnCurve.findParamFromLength( fnCurve.length() );
	
	double paramRate = maxParam/sapNum;

	double closeParam = 0.0;
	MPoint paramPoint;
	MPoint closePoint;
	MVector closeNormal;
	for( int i=0; i<= sapNum; i++ )
	{
		fnCurve.getPointAtParam( i*paramRate, paramPoint );
		paramPoint *= meshMatrix.inverse();
		fnMesh.getClosestPointAndNormal( paramPoint, closePoint, closeNormal );
		MVector paramVOnMesh = paramPoint - closePoint;

		double dotValue = paramVOnMesh*closeNormal;

		if( dotValue > 0 )
		{
			closeParam = i*paramRate;
			break;
		}
	}
	return getCloseParamOnMesh_detail( fnCurve, fnMesh, closeParam, -paramRate, meshMatrix ) ;
}


MPointArray getVtxPoints( MFnMesh& fnMesh, int polygonIndex )
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


MPointArray getStartCurvePoints( MArrayDataHandle& hArrStartEP )
{
	int length = hArrStartEP.elementCount();

	MPointArray epPoints;
	epPoints.setLength( length );

	for( int i=0; i< length; i++ )
	{
		epPoints[i] = hArrStartEP.inputValue().asVector();
		hArrStartEP.next();
	}
	return epPoints;
}


MPointArray getCurrentCurvePoints( MFnNurbsCurve& fnCurve, double cutParam, double length, MMatrix matrix, MDoubleArray& params, int& returnStartIndex, int startIndex = -1 )
{
	MPointArray paramPoints;

	double endParam   = fnCurve.findParamFromLength( length );

	int spans = fnCurve.numSpans();
	double paramRate = endParam / spans;

	MPoint eachPoint;

	double startValue = cutParam/paramRate;

	if( startIndex == -1 )
	{
		startIndex = startValue;
		if( startValue - startIndex > 0.9 )
		{
			startIndex++;
		}
	}

	returnStartIndex = startIndex;

	int pointLength = spans - startIndex + 1;
	paramPoints.setLength( pointLength );
	params.setLength( pointLength );

	fnCurve.getPointAtParam( cutParam, eachPoint );
	paramPoints[0] = eachPoint*matrix;
	params[0] = 0.0;

	int index = 1;

	for( int i=startIndex+1; i<= spans; i++ )
	{
		fnCurve.getPointAtParam( i*paramRate, eachPoint );
		paramPoints[index] = eachPoint*matrix;
		params[index] = i*paramRate-cutParam;
		index++;
	}

	return paramPoints;
}

MPointArray getCurrentCurveCVPoints( MFnNurbsCurve& fnCurve, MMatrix matrix )
{
	int cvNum = fnCurve.numCVs();

	MPointArray cvPoints;
	fnCurve.getCVs( cvPoints );

	MPoint eachPoint;
	for( int i=0; i< cvNum; i++ )
	{
		cvPoints[i] *= matrix;
	}
	return cvPoints;
}


MPointArray getBlendPoints( double constStart, double constEnd, MPointArray* pFromThisPoints, MPointArray* pToThisPoints, MMatrix matrix, MDoubleArray& params )
{	
	MPointArray& fromThisPoints = *pFromThisPoints;
	MPointArray& toThisPoints   = *pToThisPoints;

	int length = pToThisPoints->length();

	MPointArray returnPoints;
	returnPoints.setLength( length );

	double startParam = params[0];
	double paramDist  = params[ params.length()-1 ];

	for( int i=0; i< length; i++ )
	{
		double indexedParam = params[i];

		double paramValue = (indexedParam - startParam) / paramDist;
		
		double paramWeight = (paramValue-constStart)/( constEnd - constStart );

		if( paramWeight > 1 )
			paramWeight = 1;
		else if( paramWeight < 0 )
			paramWeight = 0;

		returnPoints[i] = fromThisPoints[i]*( 1-paramWeight ) + toThisPoints[i]*paramWeight;
		returnPoints[i] *= matrix;
	}

	return returnPoints;
}


MMatrix  getMatrixByPolygonIndex( MDagPath inputMeshDagPath, MObject oInputMesh, int polygonIndex )
{
	MItMeshPolygon itPolygon( inputMeshDagPath );
	MItMeshVertex  itVtx( inputMeshDagPath );
	itPolygon.reset( oInputMesh );
	itVtx.reset( oInputMesh );

	int dummyIndex;

	itPolygon.setIndex( polygonIndex, dummyIndex );

	MPointArray points;
	itPolygon.getPoints( points );

	MPoint yPoint, cPoint, xPoint;

	yPoint = points[0];
	cPoint = points[1];
	xPoint = points[2];

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



int getClosestFaceIndex( MObject oInputMesh, MPoint point, float &uValue, float &vValue )
{
	MDagPath inputMeshDagPath;
	MItMeshPolygon itPolygon( inputMeshDagPath );
	MItMeshVertex  itVtx( inputMeshDagPath );
	itPolygon.reset( oInputMesh );
	itVtx.reset( oInputMesh );

	int numPolygon = itPolygon.count();

	MIntArray vtxIndies;

	int closestIndex = 0;
	double closestLength = 10000;
	double sumLength;
	int dummyIndex;

	MPointArray points;
	for( int i=0; i< numPolygon; i++ )
	{
		itPolygon.getPoints( points );
		
		int indexLength = points.length();

		MVector sumPoint( 0,0,0 );

		for( int j=0; j< indexLength; j++ )
		{
			sumPoint += points[j];
		}
		sumPoint /= indexLength;

		sumLength = ( sumPoint - point ).length();

		if( sumLength < closestLength )
		{
			closestLength = sumLength;
			closestIndex = i;
		}
		itPolygon.next();
	}
	return closestIndex;
}



MStatus volumeCurvesOnSurface::getSurfaceInfo( MFnNurbsSurface& fnSurface, MStatus& status )
{
	int cuDegreeU = fnSurface.degreeU( &status );

	if( !status )
		return status;

	int cuDegreeV = fnSurface.degreeV();
	int cuFormU = fnSurface.formInU();
	int cuFormV = fnSurface.formInV();
	int cuNumCVsU = fnSurface.numCVsInU();
	int cuNumCVsV = fnSurface.numCVsInV();
	int cuNumSpansU = fnSurface.numSpansInU();
	int cuNumSpansV = fnSurface.numSpansInV();

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
	if( numSpansU != cuNumSpansU ){ 
		numSpansU = cuNumSpansU;
		different = true; 
	}
	if( numSpansV != cuNumSpansV ){ 
		numSpansV = cuNumSpansV;
		different = true; 
	}

	if( different )
	{
		MFnDependencyNode thisNode( thisMObject() );

		MPlug inputSurfPlug = thisNode.findPlug( "inputSurface" );

		MPlugArray connections;
		inputSurfPlug.connectedTo( connections, true, false );

		MFnDependencyNode surfNode = connections[0].node();
		
		MPlug minMaxRangeUPlug = surfNode.findPlug( "minMaxRangeU" );
		MPlug minMaxRangeVPlug = surfNode.findPlug( "minMaxRangeV" );
		
		MPlug minRangeUPlug = minMaxRangeUPlug.child( 0 );
		MPlug maxRangeUPlug = minMaxRangeUPlug.child( 1 );
		MPlug minRangeVPlug = minMaxRangeVPlug.child( 0 );
		MPlug maxRangeVPlug = minMaxRangeVPlug.child( 1 );

		minRangeU = minRangeUPlug.asDouble();
		maxRangeU = maxRangeUPlug.asDouble();
		minRangeV = minRangeVPlug.asDouble();
		maxRangeV = maxRangeVPlug.asDouble();

		centerCrvKnots = buildKnots( numCVsU, degreeU );
	}
	return MS::kSuccess;
}


MDoubleArray volumeCurvesOnSurface::buildKnots( int numCVs, int degree )
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


void volumeCurvesOnSurface::getCenterCurvePoints( MFnNurbsSurface& fnSurface, MPointArray& centerPoints, MStatus& status )
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

#endif