#include "sgIkSmoothStretch.h"
#include "sgIkSmoothStretch_def.h"

#include <maya/MPlug.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MVector.h>
#include <maya/MObject.h>

#include <maya/MGlobal.h>

#include <maya/MIOStream.h>

MTypeId     sgIkSmoothStretch::id( 0xc8d399 );

MObject sgIkSmoothStretch::aInputDistance;
MObject sgIkSmoothStretch::aInPosition;
	MObject sgIkSmoothStretch::aInPositionX;
	MObject sgIkSmoothStretch::aInPositionY;
	MObject sgIkSmoothStretch::aInPositionZ;
MObject sgIkSmoothStretch::aSmoothArea;
MObject sgIkSmoothStretch::aOutputDistance;
MObject sgIkSmoothStretch::aStretchAble;

sgIkSmoothStretch::sgIkSmoothStretch() {}
sgIkSmoothStretch::~sgIkSmoothStretch() {}


MStatus sgIkSmoothStretch::initialize()
{
	MStatus stat;

	MFnNumericAttribute nAttr;

	aInputDistance = nAttr.create( "inputDistance", "in", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( true );
	
	aInPositionX = nAttr.create( "inPositionX", "ipx", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aInPositionY = nAttr.create( "inPositionY", "ipy", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aInPositionZ = nAttr.create( "inPositionZ", "ipz", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aInPosition = nAttr.create( "inPosition", "ip", aInPositionX, aInPositionY, aInPositionZ );
	
	aOutputDistance = nAttr.create( "outputDistance", "out", MFnNumericData::kDouble, 0,0 );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aSmoothArea = nAttr.create( "smoothArea", "smoothArea", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );

	aStretchAble = nAttr.create( "stretchAble", "sa", MFnNumericData::kFloat, 1.0 );
	nAttr.setStorable( true );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1 );

	stat = addAttribute( aInputDistance );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aInPosition );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputDistance );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aStretchAble );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aSmoothArea );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( aInputDistance, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInPosition, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aStretchAble, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aSmoothArea, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	
	return MS::kSuccess;
}


MStatus sgIkSmoothStretch::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;

	if ( plug == aOutputDistance )
	{
		MArrayDataHandle hArrInputDistance = data.inputArrayValue( aInputDistance );
		MDataHandle hStretchAble = data.inputValue( aStretchAble );
		MDataHandle hSmoothArea = data.inputValue( aSmoothArea );

		float stretchAble = hStretchAble.asFloat();

		double allDistance = 0.0;
		int arrayCount = hArrInputDistance.elementCount();

		double* outputDistances = new double[arrayCount]; 

		int multMinus = 1;
		for( int i=0; i<arrayCount; i++ )
		{
			MDataHandle hInputDistance = hArrInputDistance.inputValue();
			double inputDistance = hInputDistance.asDouble();

			if( inputDistance < 0 )
			{
				multMinus = -1;
				outputDistances[i] = -inputDistance;
			}
			else
			{
				outputDistances[i] = inputDistance;
			}
			allDistance += outputDistances[i];
			hArrInputDistance.next();
		}
		
		MDataHandle hInPosition = data.inputValue( aInPosition );
		MDataHandle hInPositionX = hInPosition.child( aInPositionX );
		MDataHandle hInPositionY = hInPosition.child( aInPositionY );
		MDataHandle hInPositionZ = hInPosition.child( aInPositionZ );

		double smoothArea = hSmoothArea.asDouble()*0.1;

		double poseDistance = sqrt( pow( hInPositionX.asDouble(), 2 )+pow( hInPositionY.asDouble(), 2 )+pow( hInPositionZ.asDouble(), 2 ) ) ;
		allDistance = fabs( allDistance );

		double stretchRate = getSmoothStretchRate( outputDistances[0], outputDistances[1], poseDistance, smoothArea );
		double smoothRate  = getSmoothRate( outputDistances[0], outputDistances[1], poseDistance, smoothArea );

		double currentRate = ( 1-stretchAble )*smoothRate + stretchAble*stretchRate;

		outputDistances[0] *= currentRate*multMinus;
		outputDistances[1] *= currentRate*multMinus;

		MArrayDataHandle hArrOutputDistance = data.outputArrayValue( aOutputDistance );
		MArrayDataBuilder bArrOutputDistance( aOutputDistance, arrayCount, &stat );

		for( int i=0; i<arrayCount; i++ )
		{
			MDataHandle hOutputDistance = bArrOutputDistance.addElement( i );
			hOutputDistance.set( outputDistances[i] );
		}

		hArrOutputDistance.set( bArrOutputDistance );
		hArrOutputDistance.setAllClean();

		data.setClean( plug );
	}
	return MS::kSuccess;
}

void* sgIkSmoothStretch::creator()
{
	return new sgIkSmoothStretch();
}