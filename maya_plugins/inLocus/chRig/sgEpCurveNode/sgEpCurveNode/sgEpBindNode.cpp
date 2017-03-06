#include "sgEpBindNode.h"

#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MMatrixArray.h>
#include <maya/MPointArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MGlobal.h>

MTypeId     sgEpBindNode::id( 0xc8cc01 );


MObject     sgEpBindNode::aEnvelope;
MObject     sgEpBindNode::aInputPoint;
	MObject     sgEpBindNode::aInputPointX;
	MObject     sgEpBindNode::aInputPointY;
	MObject     sgEpBindNode::aInputPointZ;
MObject     sgEpBindNode::aMatrix;
MObject     sgEpBindNode::aOrigMatrix;
MObject     sgEpBindNode::aOutputs;
	MObject     sgEpBindNode::aOutputCurve;
	MObject     sgEpBindNode::aOutputPoint;
		MObject     sgEpBindNode::aOutputPointX;
		MObject     sgEpBindNode::aOutputPointY;
		MObject     sgEpBindNode::aOutputPointZ;

sgEpBindNode::sgEpBindNode() {}
sgEpBindNode::~sgEpBindNode() {}

struct indexAndDist
{
	int index;
	double distance;
};

indexAndDist* getTwoClosestMtxIndies( MPoint& point, MMatrixArray& mtxArr )
{
	int length = mtxArr.length();

	int firstIndex = 0;
	int secondIndex = 1;

	double firstDist = 100000;
	double secondDist = 100000;

	for( int i=0; i< length; i++ )
	{
		MPoint mtxPoint( mtxArr[i](3,0), mtxArr[i](3,1), mtxArr[i](3,2) );

		double dist = mtxPoint.distanceTo( point );
		
		if(  dist < firstDist )
		{
			secondIndex = firstIndex;
			secondDist = firstDist;
			firstIndex = i;
			firstDist = dist;
		}

		if( dist < secondDist )
		{
			if( firstIndex != i )
			{
				secondIndex = i;
				secondDist = dist;
			}
		}
	}

	indexAndDist* returnValue = new indexAndDist[2];

	returnValue[0].index    = firstIndex;
	returnValue[0].distance = firstDist;
	returnValue[1].index    = secondIndex;
	returnValue[1].distance = secondDist;

	return returnValue;
}


MPoint getProperPoint( MMatrixArray& mts, MMatrixArray& origMts, MPoint point )
{
	if( mts.length() < 2 || origMts.length() < 2 ) return point;
	indexAndDist* indexAndDistPtr = getTwoClosestMtxIndies( point, origMts );

	MMatrix mtx1 = origMts[ indexAndDistPtr[0].index ].inverse()*mts[ indexAndDistPtr[0].index ];
	MMatrix mtx2 = origMts[ indexAndDistPtr[1].index ].inverse()*mts[ indexAndDistPtr[1].index ];

	float w1, w2;

	if( indexAndDistPtr[0].distance == 0 )
	{
		w1 = 1;
		w2 = 0;
	}
	else if( indexAndDistPtr[1].distance == 0 )
	{
		w1 = 0;
		w2 = 1;
	}
	else
	{
		float w1Value= indexAndDistPtr[1].distance / indexAndDistPtr[0].distance;
		float w2Value = indexAndDistPtr[0].distance / indexAndDistPtr[1].distance;

		float w1Value_av = indexAndDistPtr[1].distance / (indexAndDistPtr[0].distance + indexAndDistPtr[1].distance );
		float w2Value_av = indexAndDistPtr[0].distance / (indexAndDistPtr[0].distance + indexAndDistPtr[1].distance );

		if( w1Value < 0.001 )
		{
			w1 = 0;
			w2 = 1;
		}
		else if( w2Value < 0.001 )
		{
			w1 = 1;
			w2 = 0;
		}
		else
		{
			w1 = w1Value_av; // w1Value/(w1Value+w2Value);
			w2 = w2Value_av; //w2Value/(w1Value+w2Value);
		}
	}
	delete []indexAndDistPtr;
	return point*( mtx1*w1 + mtx2*w2 );
}


MStatus sgEpBindNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;

	if( plug != aOutputCurve && plug != aOutputPoint ){return MS::kFailure;}
	
	MDataHandle hEnvelope = data.inputValue( aEnvelope );

	MArrayDataHandle hArrMatrix     = data.inputArrayValue( aMatrix );
	MArrayDataHandle hArrOrgMatrix  = data.inputArrayValue( aOrigMatrix );

	MArrayDataHandle hArrInputPoint = data.inputValue( aInputPoint );

	int mtxLength    = hArrMatrix.elementCount();
	int orgMtxLength = hArrOrgMatrix.elementCount();
	int pointLength  = hArrInputPoint.elementCount();

	if( orgMtxLength != mtxLength ){return MS::kFailure;}

	MMatrixArray mts;
	MMatrixArray orgMts;
	mts.setLength( mtxLength );
	orgMts.setLength( orgMtxLength );

	for( int i=0; i< mtxLength; i++ )
	{
		MDataHandle hMatrix = hArrMatrix.inputValue();
		MDataHandle hOrgMatrix = hArrOrgMatrix.inputValue();

		MMatrix mtx = hMatrix.asMatrix();
		MMatrix orgMtx = hOrgMatrix.asMatrix();

		mts.set( mtx, i );
		orgMts.set( orgMtx, i );

		hArrMatrix.next();
		hArrOrgMatrix.next();
	}

	MPointArray points;
	points.setLength( pointLength );

	float env = hEnvelope.asFloat();
	for( int i=0; i < pointLength; i++, hArrInputPoint.next() )
	{
		MDataHandle hInputPoint = hArrInputPoint.inputValue();
		MPoint inputPoint( hInputPoint.asVector() );

		MPoint movedPoint = getProperPoint( mts, orgMts, inputPoint );
		points.set( movedPoint*env + inputPoint*(1-env), i );
	}

	MFnDependencyNode fnNode( thisMObject() );

	MPlugArray connections;
	MPlug outputCurvePlug = fnNode.findPlug( aOutputCurve );
	outputCurvePlug.connectedTo( connections, false, true );

	if( connections.length() != 0 )
	{
		MFnNurbsCurveData dOutputCurve;
		MObject outputCurveObject = dOutputCurve.create();

		MFnNurbsCurve outputCurve;

		outputCurve.createWithEditPoints( points, 3, MFnNurbsCurve::kOpen, false, false, true, outputCurveObject, &stat );
		if( !stat ){ stat.perror( "can't not create curve!" ); return stat; }

		MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
		hOutputCurve.set( outputCurveObject );
	}

	if( plug == aOutputPoint )
	{	
		MArrayDataHandle hArrOutputPoint = data.outputArrayValue( aOutputPoint );
		MArrayDataBuilder builder( aOutputPoint, pointLength, &stat );
		CHECK_MSTATUS_AND_RETURN_IT( stat );

		for( int i=0; i< pointLength; i++ )
		{
			MDataHandle hOutputPoint = builder.addElement( i );
			hOutputPoint.set( points[i].x, points[i].y, points[i].z );
		}
		hArrOutputPoint.set( builder );
		hArrOutputPoint.setAllClean();
	}

	data.setClean( plug );

	return MS::kSuccess;
}

void* sgEpBindNode::creator()
{
	return new sgEpBindNode();
}

MStatus sgEpBindNode::initialize()		
{
	MFnCompoundAttribute cAttr;
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnTypedAttribute tAttr;
	MStatus				stat;

	aEnvelope = nAttr.create( "envelope", "evn", MFnNumericData::kFloat, 1 );
	nAttr.setMin( 0 );
	nAttr.setMax( 1 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );

	aInputPointX = nAttr.create( "inputPointX", "ipx", MFnNumericData::kDouble, 0.0 );
	aInputPointY = nAttr.create( "inputPointY", "ipy", MFnNumericData::kDouble, 0.0 );
	aInputPointZ = nAttr.create( "inputPointZ", "ipz", MFnNumericData::kDouble, 0.0 );
	aInputPoint = nAttr.create( "inputPoint", "ip", aInputPointX, aInputPointY, aInputPointZ );
	nAttr.setArray( true );
	nAttr.setStorable( true );

	aMatrix = mAttr.create( "matrix", "m" );
	mAttr.setArray( true );
	mAttr.setStorable( true );

	aOrigMatrix = mAttr.create( "origMatrix", "om" );
	mAttr.setArray( true );
 	mAttr.setStorable(false);

	aOutputs = cAttr.create( "outputs", "outs" );
		aOutputCurve = tAttr.create( "outputCurve", "oc", MFnData::kNurbsCurve );

		aOutputPointX = nAttr.create( "outputPointX", "opx", MFnNumericData::kDouble, 0.0 );
		aOutputPointY = nAttr.create( "outputPointY", "opy", MFnNumericData::kDouble, 0.0 );
		aOutputPointZ = nAttr.create( "outputPointZ", "opz", MFnNumericData::kDouble, 0.0 );
		aOutputPoint = nAttr.create( "outputPoint", "op", aOutputPointX, aOutputPointY, aOutputPointZ );
		nAttr.setArray( true );
		nAttr.setUsesArrayDataBuilder( true );

	cAttr.addChild( aOutputCurve );
	cAttr.addChild( aOutputPoint );


	stat = addAttribute( aEnvelope );
		if (!stat) { stat.perror("addAttribute degree"); return stat;}
	stat = addAttribute( aInputPoint );
		if (!stat) { stat.perror("addAttribute inputPoint"); return stat;}
	stat = addAttribute( aMatrix );
		if (!stat) { stat.perror("addAttribute matrix"); return stat;}
	stat = addAttribute( aOrigMatrix );
		if (!stat) { stat.perror("addAttribute origMatrix"); return stat;}
	stat = addAttribute( aOutputs );
		if (!stat) { stat.perror("addAttribute outputPoint"); return stat;}

	stat = attributeAffects( aEnvelope, aOutputs );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInputPoint, aOutputs );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix, aOutputs );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aOrigMatrix, aOutputs );
		if (!stat) { stat.perror("attributeAffects"); return stat;}


	return MS::kSuccess;
}