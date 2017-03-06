#include "controlerShape.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MDoubleArray.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MEulerRotation.h>

#include <maya/MVector.h>

#define QUADRANGLE 0
#define BOX        1
#define SWITCH     2
#define EYE        3
#define FLY        4
#define BAR        5
#define MOVE       6
#define PIN        7
#define SPHERE     8

MTypeId controlerShape::id( 0xc8c913 );

MObject  controlerShape::aControlerType;

MObject  controlerShape::aOffset;
	MObject  controlerShape::aOffsetX;
	MObject  controlerShape::aOffsetY;
	MObject  controlerShape::aOffsetZ;
MObject  controlerShape::aOrient;
	MObject  controlerShape::aOrientX;
	MObject  controlerShape::aOrientY;
	MObject  controlerShape::aOrientZ;
MObject  controlerShape::aSize;
	MObject  controlerShape::aSizeX;
	MObject  controlerShape::aSizeY;
	MObject  controlerShape::aSizeZ;

MObject  controlerShape::aOutputCurve;

controlerShape::controlerShape() {};
controlerShape::~controlerShape() {};

double quadranglePointData[6][3] = 
{ 1,0,-1, 1,0,1, -1,0,1, -1,0,-1, 1,0,-1, 0,0,0 };

double boxPointData[18][3] = 
{ -1,-1,-1, -1,1,-1, -1,1,1, -1,-1,1, -1,-1,-1, 1,-1,-1, 1,1,-1, -1,1,-1, -1,1,1, 1,1,1,
1,-1,1, -1,-1,1, -1,1,1, 1,1,1, 1,1,-1, 1,-1,-1, 1,-1,1, 0,0,0};

double switchPointData[16][3] = 
{ 0, 0.001, 0,  2, 2, 0,  1, 2, 0,  1, 4, 0,  -1, 4, 0,  -1, 2, 0,  -2, 2, 0,  0, 0.001, 0,  0, 2, -2,  0, 2, -1,  0, 4, -1,  0, 4, 1,  0, 2, 1,  0, 2, 2,  0, 0.001, 0, 0,0,0 };

double eyePointData[18][3] = 
{0,0,-0.42871, -0.42871,0,-0.42871, -0.857421,0,-0.857421, -1.714841,0,-0.857421, -2.143552,0,0, -1.714841,0,0.857421,
-0.857421,0,0.857421, -0.42871,0,0.42871, 0,0,0.42871, 0.42871,0,0.42871, 0.857421,0,0.857421, 1.714841,0,0.857421, 
2.143552,0,0, 1.714841,0,-0.857421, 0.857421,0,-0.857421,0.42871,0,-0.42871, 0,0,-0.42871, 0,0,0};

double flyPointData[8][3] = 
{-2, 0, 0,  0, 0, -2,  2, 0, 0,  1, 0, 0,  0, 0, -1,  -1, 0, 0,  -2, 0, 0,  0, 0, 0};

double barPointData[15][3] = 
{0,0,-0.49092, -1,0,-0.49092, -1.492134,0,-0.98184, -2,0,-0.49092, -2,0,0.49092, -1.492134,0,0.98184, -1,0,0.49092,
1,0,0.49092, 1.492134,0,0.98184, 2,0,0.49092, 2,0,-0.49092, 1.492134,0,-0.98184, 1,0,-0.49092, 0,0,-0.49092, 0,0,0};

double movePointData[26][3] = 
{0,0,-2, -0.590146,0,-1, -0.295073,0,-1, -0.295073,0,-0.295073, -1,0,-0.295073, -1,0,-0.590146, -2,0,0, -1,0,0.590146,
-1,0,0.295073, -0.295073,0,0.295073, -0.295073,0,1, -0.590146,0,1, 0,0,2, 0.590146,0,1, 0.295073,0,1, 0.295073,0,0.295073,
1,0,0.295073, 1,0,0.590146, 2,0,0, 1,0,-0.590146, 1,0,-0.295073, 0.295073,0,-0.295073, 0.295073,0,-1, 0.590146,0,-1, 0,0,-2, 0,0,0 };

double pinPointData[13][3] = 
{ 0,0.001,0,  0,1.2,0,  -0.235114,1.276393,0,  -0.380423,1.476393,0,  -0.380423,1.723607,0,  -0.235114,1.923607,0, 
  0,2,0,  0.235114,1.923607,0,  0.380423,1.723607,0,  0.380423,1.476393,0,  0.235114,1.276393,0,  0,1.2,0, 0,0,0 };

double spherePointData[54][3] = 
{ 0,1,0, -0.382683,0.92388,0, -0.707107,0.707107,0, -0.92388,0.382683,0, -1,0,0, -0.92388,-0.382683,0, -0.707107,-0.707107,0,
-0.382683,-0.92388,0, 0,-1,0, 0.382683,-0.92388,0, 0.707107,-0.707107,0, 0.92388,-0.382683,0, 1,0,0, 0.92388,0.382683,0, 0.707107,0.707107,0, 
0.382683,0.92388,0, 0,1,0, 0,0.92388,0.382683, 0,0.707107,0.707107, 0,0.382683,0.92388, 0,0,1, 0,-0.382683,0.92388, 0,-0.707107,0.707107, 0,-0.92388,0.382683, 
0,-1,0, 0,-0.92388,-0.382683, 0,-0.707107,-0.707107, 0,-0.382683,-0.92388, 0,0,-1, 0,0.382683,-0.92388, 0,0.707107,-0.707107, 0,0.92388,-0.382683, 0,1,0, 
-0.382683,0.92388,0, -0.707107,0.707107,0, -0.92388,0.382683,0, -1,0,0, -0.92388,0,0.382683, -0.707107,0,0.707107, -0.382683,0,0.92388, 
0,0,1, 0.382683,0,0.92388, 0.707107,0,0.707107, 0.92388,0,0.382683, 1,0,0, 0.92388,0,-0.382683, 0.707107,0,-0.707107, 0.382683,0,-0.92388, 0,0,-1, -0.382683,0,-0.92388,
-0.707107,0,-0.707107, -0.92388,0,-0.382683, -1,0,0, 0,0,0 };

int minKnotIndex =0;
int maxKnotIndex;

MPointArray buildControlPoints( double doubleValues[][3] )
{
	MPointArray pointArr;

	int i = 0;
	while( true )
	{
		MPoint pointValue( doubleValues[i][0], doubleValues[i][1], doubleValues[i][2] );
		MVector pointVector( pointValue );
		if( pointVector.length() < 0.00001 )
			break;
		pointArr.append( pointValue );
		i++;
	}
	return pointArr;
}

MDoubleArray buildKnots( double doubleValues[][3], int degree = 1 )
{
	MDoubleArray doubleArr;
	double value;
	int i = 0;

	if( degree == 3 )
		doubleArr.append( 0.0 );

	while( true )
	{
		if( doubleValues[i][0] == 0 && doubleValues[i][1] == 0 &&  doubleValues[i][2] == 0 )   
			break;
		doubleArr.append( ( double )i );
		value = i;
		maxKnotIndex = i;
		i++;
	}

	if( degree == 3 )
		doubleArr.append( (double)maxKnotIndex );

	return doubleArr;
}

void transformControlPoints( MPointArray& pointArr, MMatrix matrix )
{
	for( int i=0; i < pointArr.length(); i++ )
		pointArr[i] *= matrix;
}

MStatus controlerShape::initialize()
{
	MStatus stat;

	MFnEnumAttribute eAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;
	MFnTypedAttribute tAttr;
	
	aControlerType= eAttr.create( "controlerType", "ct" );
	eAttr.addField( "Quadrangle", QUADRANGLE );
	eAttr.addField( "Box", BOX );
	eAttr.addField( "Switch", SWITCH );
	eAttr.addField( "Eye", EYE );
	eAttr.addField( "Fly", FLY );
	eAttr.addField( "Bar", BAR );
	eAttr.addField( "Move", MOVE );
	eAttr.addField( "Pin", PIN );
	eAttr.addField( "Sphere", SPHERE );
	eAttr.setStorable( true );

	aOffsetX = nAttr.create( "offsetX", "ofx", MFnNumericData::kDouble, 0.0 );
	aOffsetY = nAttr.create( "offsetY", "ofy", MFnNumericData::kDouble, 0.0 );
	aOffsetZ = nAttr.create( "offsetZ", "ofz", MFnNumericData::kDouble, 0.0 );
	aOffset = nAttr.create( "offset", "of", aOffsetX, aOffsetY, aOffsetZ );
	nAttr.setStorable( true );
	nAttr.setWritable( true );

	aOrientX = uAttr.create( "orientX", "orx", MFnUnitAttribute::kAngle, 0.0 );
	aOrientY = uAttr.create( "orientY", "ory", MFnUnitAttribute::kAngle, 0.0 );
	aOrientZ = uAttr.create( "orientZ", "orz", MFnUnitAttribute::kAngle, 0.0 );
	aOrient = nAttr.create( "orient", "or", aOrientX, aOrientY, aOrientZ );
	nAttr.setStorable( true );
	nAttr.setWritable( true );
	
	aSizeX = nAttr.create( "sizeX", "sx", MFnNumericData::kDouble, 1 );
	aSizeY = nAttr.create( "sizeY", "sy", MFnNumericData::kDouble, 1 );
	aSizeZ = nAttr.create( "sizeZ", "sz", MFnNumericData::kDouble, 1 );
	aSize = nAttr.create( "size", "s", aSizeX, aSizeY, aSizeZ );
	nAttr.setStorable( true );
	nAttr.setWritable( true );

	aOutputCurve = tAttr.create( "outputCurve", "oc", MFnData::kNurbsCurve );
	tAttr.setStorable( false );

	stat = addAttribute( aControlerType );
	if( !stat ){ stat.perror( "addAttribute : aControlerType" ); return stat; }
	stat = addAttribute( aOffset );
	if( !stat ){ stat.perror( "addAttribute : aOffset" ); return stat; }
	stat = addAttribute( aOrient );
	if( !stat ){ stat.perror( "addAttribute : aOrient" ); return stat; }
	stat = addAttribute( aSize );
	if( !stat ){ stat.perror( "addAttribute : aSize" ); return stat; }
	stat = addAttribute( aOutputCurve );
	if( !stat ){ stat.perror( "addAttribute : aOutputCurve" ); return stat; }

	stat = attributeAffects( aControlerType, aOutputCurve );
	if( !stat ){ stat.perror( "attributeAffects : aControlerType" ); return stat; }
	stat = attributeAffects( aOffset, aOutputCurve );
	if( !stat ){ stat.perror( "attributeAffects : aOffset" ); return stat; }
	stat = attributeAffects( aOrient, aOutputCurve );
	if( !stat ){ stat.perror( "attributeAffects : aOrient" ); return stat; }
	stat = attributeAffects( aSize, aOutputCurve );
	if( !stat ){ stat.perror( "attributeAffects : aSize" ); return stat; }

	return MS::kSuccess;
}

MStatus controlerShape::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MDataHandle hControlerType = block.inputValue( aControlerType );
	MPointArray shapePoints;
	MDoubleArray knots;
	int degree = 1;

	switch( hControlerType.asInt() )
	{
	case QUADRANGLE:
		shapePoints = buildControlPoints( quadranglePointData );
		knots       = buildKnots( quadranglePointData );
		break;
	case BOX:
		shapePoints = buildControlPoints( boxPointData );
		knots       = buildKnots( boxPointData );
		break;
	case SWITCH:
		shapePoints = buildControlPoints( switchPointData );
		knots       = buildKnots( switchPointData );
		break;
	case EYE:
		shapePoints = buildControlPoints( eyePointData );
		knots       = buildKnots( eyePointData, 3 );
		degree = 3;
		break;
	case FLY:
		shapePoints = buildControlPoints( flyPointData );
		knots       = buildKnots( flyPointData );
		break;
	case BAR:
		shapePoints = buildControlPoints( barPointData );
		knots       = buildKnots( barPointData );
		break;
	case MOVE:
		shapePoints = buildControlPoints( movePointData );
		knots       = buildKnots( movePointData );
		break;
	case PIN:
		shapePoints = buildControlPoints( pinPointData );
		knots       = buildKnots( pinPointData );
		break;
	case SPHERE:
		shapePoints = buildControlPoints( spherePointData );
		knots       = buildKnots( spherePointData );
		break;
	}

	MDataHandle hOffset = block.inputValue( aOffset );
	MDataHandle hOrient = block.inputValue( aOrient );
	MDataHandle hSize   = block.inputValue( aSize );

	MEulerRotation eulerRot( hOrient.asVector() );

	MPxTransformationMatrix curveBodyMtx;
	MPxTransformationMatrix curveTransMtx;
	curveBodyMtx.rotateTo( eulerRot );
	curveBodyMtx.scaleTo( hSize.asVector() );
	curveTransMtx.translateTo( hOffset.asVector() );
	MMatrix curveMatrix = curveBodyMtx.asMatrix()*curveTransMtx.asMatrix();

	transformControlPoints( shapePoints, curveMatrix );

	MFnNurbsCurve outputCurve;
	MFnNurbsCurveData dOutputCurve;
	MObject outputCurveObject = dOutputCurve.create();

	MObject curveObject = outputCurve.create( shapePoints, knots, degree, MFnNurbsCurve::kOpen, 0,0, outputCurveObject, &stat );
	if( !stat ){ stat.perror( "can't not create curve!" ); return stat; }

	MDataHandle hOutputCurve = block.outputValue( aOutputCurve );
	hOutputCurve.set( outputCurveObject );

	block.setClean(plug);
	
	return MS::kSuccess;
}


void* controlerShape::creator()
{
	return new controlerShape();
}