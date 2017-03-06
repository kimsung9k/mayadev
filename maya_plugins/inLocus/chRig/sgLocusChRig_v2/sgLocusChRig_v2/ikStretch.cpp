#include "ikStretch.h"

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

MTypeId     ikStretch::id( 0xc8c903 );

MObject ikStretch::aInputDistance;
MObject ikStretch::aInPosition;
	MObject ikStretch::aInPositionX;
	MObject ikStretch::aInPositionY;
	MObject ikStretch::aInPositionZ;
MObject ikStretch::aOutputDistance;
MObject ikStretch::aStretchAble;

ikStretch::ikStretch() {}
ikStretch::~ikStretch() {}

MStatus ikStretch::initialize()
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

	stat = attributeAffects( aInputDistance, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInPosition, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aStretchAble, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	
	return MS::kSuccess;
}

MStatus ikStretch::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;

	if ( plug == aOutputDistance )
	{
		MArrayDataHandle hArrInputDistance = data.inputArrayValue( aInputDistance );

		double allDistance = 0.0;
		int arrayCount = hArrInputDistance.elementCount();

		double* outputDistances = new double[arrayCount]; 

		for( int i=0; i<arrayCount; i++ )
		{
			MDataHandle hInputDistance = hArrInputDistance.inputValue();
			double inputDistance = hInputDistance.asDouble();
			outputDistances[i]= inputDistance;
			allDistance += inputDistance;
			hArrInputDistance.next();
		}
		
		MDataHandle hInPosition = data.inputValue( aInPosition );
		MDataHandle hInPositionX = hInPosition.child( aInPositionX );
		MDataHandle hInPositionY = hInPosition.child( aInPositionY );
		MDataHandle hInPositionZ = hInPosition.child( aInPositionZ );

		double poseDistance = sqrt( pow( hInPositionX.asDouble(), 2 )+pow( hInPositionY.asDouble(), 2 )+pow( hInPositionZ.asDouble(), 2 ) );
		allDistance = fabs( allDistance );

		if( allDistance < poseDistance && allDistance > 0 )
		{
			double stratchRate = poseDistance/allDistance;
			MDataHandle hStretchAble = data.inputValue( aStretchAble );
			float stretchAble = hStretchAble.asFloat();

			for( int i=0; i<arrayCount; i++ )
			{
				double diff = outputDistances[i] * stratchRate - outputDistances[i];
				outputDistances[i] += diff*stretchAble;
			}
		}

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

void* ikStretch::creator()
{
	return new ikStretch();
}