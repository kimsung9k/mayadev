#include "sgEpCurveNode.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MMatrix.h>
#include <maya/MPointArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MGlobal.h>

MTypeId     sgEpCurveNode::id( 0xc8cc02 );

MObject     sgEpCurveNode::aInputPoint;
	MObject     sgEpCurveNode::aInputPointX;
	MObject     sgEpCurveNode::aInputPointY;
	MObject     sgEpCurveNode::aInputPointZ;
MObject     sgEpCurveNode::aDegree;
MObject     sgEpCurveNode::aOutputCurve;


sgEpCurveNode::sgEpCurveNode() {}
sgEpCurveNode::~sgEpCurveNode() {}


MStatus sgEpCurveNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;

	if( plug != aOutputCurve ){return MS::kFailure;}
	
	MArrayDataHandle hArrInputPoint = data.inputArrayValue( aInputPoint );
	
	int arrLength = hArrInputPoint.elementCount();

	MPointArray points;
	points.setLength( arrLength );

	//cout << arrLength << endl;
	for( int i=0; i < arrLength; i++ )
	{
		MDataHandle hInputPoint = hArrInputPoint.inputValue();
		MPoint point = hInputPoint.asVector();

		//cout << "Points " << mat(3,0) <<" "<< mat(3,1) <<" "<< mat(3,2) << i << endl;
		points.set( i, point.x,point.y ,point.z );

		hArrInputPoint.next();
	}

	MFnNurbsCurveData dOutputCurve;
	MObject outputCurveObject = dOutputCurve.create();

	MFnNurbsCurve outputCurve;

	MDataHandle hDegree = data.inputValue( aDegree );

	outputCurve.createWithEditPoints( points, hDegree.asInt(), MFnNurbsCurve::kOpen, false, false, true, outputCurveObject, &stat );
	if( !stat ){ stat.perror( "can't not create curve!" ); return stat; }

	MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
	hOutputCurve.set( outputCurveObject );

	data.setClean( plug );
	return MS::kSuccess;
}

void* sgEpCurveNode::creator()
{
	return new sgEpCurveNode();
}

MStatus sgEpCurveNode::initialize()		
{
	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;
	MStatus				stat;

	aInputPointX = nAttr.create( "inputPointX", "ipx", MFnNumericData::kDouble, 0.0 );
	aInputPointY = nAttr.create( "inputPointY", "ipy", MFnNumericData::kDouble, 0.0 );
	aInputPointZ = nAttr.create( "inputPointZ", "ipz", MFnNumericData::kDouble, 0.0 );
	aInputPoint = nAttr.create( "inputPoint", "ip", aInputPointX, aInputPointY, aInputPointZ );
	nAttr.setArray( true );
 	nAttr.setStorable(false);

	aDegree = nAttr.create( "degree", "d", MFnNumericData::kInt, 3 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );

	aOutputCurve = tAttr.create( "outputCurve", "oc", MFnData::kNurbsCurve );
	tAttr.setStorable( false );

	stat = addAttribute( aInputPoint );
	CHECK_MSTATUS_AND_RETURN_IT( stat );
	stat = addAttribute( aDegree );
	CHECK_MSTATUS_AND_RETURN_IT( stat );
	stat = addAttribute( aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( stat );

	stat = attributeAffects( aInputPoint, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( stat );
	stat = attributeAffects( aDegree, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( stat );

	return MS::kSuccess;
}

