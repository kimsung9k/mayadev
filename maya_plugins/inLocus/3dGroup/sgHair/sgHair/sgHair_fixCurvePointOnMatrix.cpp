#include "sgHair_fixCurvePointOnMatrix.h"

#include <maya/MGlobal.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

MTypeId   sgHair_fixCurvePointOnMatrix::id( 0xd8c104 );

MObject   sgHair_fixCurvePointOnMatrix::aBaseMatrix;

MObject   sgHair_fixCurvePointOnMatrix::aInputCurve;

MObject   sgHair_fixCurvePointOnMatrix::aConstStart;
MObject   sgHair_fixCurvePointOnMatrix::aConstEnd;

MObject   sgHair_fixCurvePointOnMatrix::aConstPoint;
	MObject   sgHair_fixCurvePointOnMatrix::aConstPointX;
	MObject   sgHair_fixCurvePointOnMatrix::aConstPointY;
	MObject   sgHair_fixCurvePointOnMatrix::aConstPointZ;

MObject   sgHair_fixCurvePointOnMatrix::aOutputCurve;


sgHair_fixCurvePointOnMatrix::sgHair_fixCurvePointOnMatrix(){};
sgHair_fixCurvePointOnMatrix::~sgHair_fixCurvePointOnMatrix(){};


void*  sgHair_fixCurvePointOnMatrix::creator()
{
	return new sgHair_fixCurvePointOnMatrix();
}


MPoint getBlendPoint( float blendPosition, float constEnd, MPoint point1, MPoint point2, int pointIndex )
{
	float startPosition = blendPosition;

	float indexPosition = pointIndex - startPosition;

	if( indexPosition < 0 )
		return point1;
	if( pointIndex - startPosition - constEnd > 0 )
		return point2;

	float indexRate = indexPosition/constEnd;

	float resultRate;
	if( indexRate > 0.5 )
	{
		float cuRate = (indexRate - 0.5)*2;
		resultRate = ( 1 - pow( 1-cuRate,2 ) )*0.5 + 0.5;
	}
	else
	{
		float cuRate = indexRate*2;
		resultRate = pow( cuRate, 2 )*0.5;
	}

	//cout << blendPosition << " : " << constEnd << endl;
	//cout << "resultRate[" << pointIndex << "] : " << resultRate << endl;

	return point1*( 1-resultRate ) + point2*resultRate;
}


MStatus sgHair_fixCurvePointOnMatrix::compute( const MPlug& plug,  MDataBlock& data )
{
	MStatus status;

	MDataHandle hOutputCurve = data.outputValue( aOutputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hBaseMatrix = data.inputValue( aBaseMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputCurve = data.inputValue( aInputCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hConstStart = data.inputValue( aConstStart, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hConstEnd = data.inputValue( aConstEnd, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MArrayDataHandle hArrConstPoint = data.inputArrayValue( aConstPoint, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix baseMatrix = hBaseMatrix.asMatrix();
	MFnNurbsCurve inputCurve = hInputCurve.asNurbsCurve();
	float constStart = hConstStart.asFloat();
	float constEnd     = hConstEnd.asFloat();

	MPoint rootPoint;
	MPoint anglePoint;

	MPointArray inputCVs;
	inputCurve.getCVs( inputCVs );

	////////////////////////////////////////////////////////////////////////////

	int inputCVsLength = inputCVs.length();

	if( inputCVsLength > hArrConstPoint.elementCount() )
	{
		MFnDependencyNode thisNode = thisMObject();
		
		MPlug constPointPlug = thisNode.findPlug( aConstPoint );

		for( int i=0; i < inputCVsLength; i++ )
		{
			MPlug constPointElement = constPointPlug.elementByLogicalIndex( i );

			MPoint localPoint = inputCVs[i] * baseMatrix.inverse();

			constPointElement.child( aConstPointX ).setDouble( localPoint.x );
			constPointElement.child( aConstPointY ).setDouble( localPoint.y );
			constPointElement.child( aConstPointZ ).setDouble( localPoint.z );
		}
		hArrConstPoint = data.inputArrayValue( aConstPoint, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	//////////////////////////////////////////////////////////////////////////

	for( int i=0; i< inputCVsLength; i++ )
	{
		MPoint localCV = inputCVs[i] * baseMatrix.inverse();
		hArrConstPoint.jumpToElement( i );
		MVector constPoint = hArrConstPoint.inputValue().asVector();

		MPoint setPoint = getBlendPoint( hConstStart.asFloat(), hConstEnd.asFloat(), constPoint, localCV, i );

		//cout << "setPoint : " << setPoint << endl;
		//cout << "localCV : " << localCV << endl;

		inputCVs[i] = setPoint * baseMatrix;
	}

	MFnNurbsCurveData dOutputCurve;
	MObject outputCurveObject = dOutputCurve.create();

	MDoubleArray knots;
	inputCurve.getKnots( knots );

	MObject curveObject = inputCurve.create( inputCVs, knots, inputCurve.degree(), MFnNurbsCurve::kOpen, 0,0, outputCurveObject, &status  );
	if( !status ){ status.perror( "can't not create curve!" ); return status; }

	MFnNurbsCurve fnOutputCurve( outputCurveObject );
	fnOutputCurve.updateCurve();

	hOutputCurve.set( outputCurveObject );

	data.setClean( plug );

	return MS::kSuccess;
}


MStatus  sgHair_fixCurvePointOnMatrix::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;
	MFnMatrixAttribute mAttr;

	aOutputCurve = tAttr.create( "outputCurve", "oc", MFnData::kNurbsCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	tAttr.setStorable( false );
	status = addAttribute( aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aInputCurve = tAttr.create( "inputCurve", "ic", MFnData::kNurbsCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	tAttr.setStorable( true );
	status = addAttribute( aInputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aInputCurve, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aBaseMatrix = mAttr.create( "baseMatrix", "bmat", MFnMatrixAttribute::kDouble, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	mAttr.setStorable( true );
	status = addAttribute( aBaseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aBaseMatrix, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aConstStart = nAttr.create( "constStart", "cons", MFnNumericData::kFloat, 0.0f, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	nAttr.setMin( 0.0f );
	status = addAttribute( aConstStart );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aConstStart, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aConstEnd = nAttr.create( "constEnd", "cone", MFnNumericData::kFloat, 1.0f, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	nAttr.setMin( 0.0f );
	status = addAttribute( aConstEnd );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aConstEnd, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aConstPointX = nAttr.create( "constPointX", "cpx", MFnNumericData::kDouble, 0.0, &status );
	aConstPointY = nAttr.create( "constPointY", "cpy", MFnNumericData::kDouble, 0.0, &status );
	aConstPointZ = nAttr.create( "constPointZ", "cpz", MFnNumericData::kDouble, 0.0, &status );
	aConstPoint  = nAttr.create( "constPoint", "cp", aConstPointX, aConstPointY, aConstPointZ, &status );
	nAttr.setStorable( true );
	nAttr.setArray( true );
	status = addAttribute( aConstPoint );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aConstPoint, aOutputCurve );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}