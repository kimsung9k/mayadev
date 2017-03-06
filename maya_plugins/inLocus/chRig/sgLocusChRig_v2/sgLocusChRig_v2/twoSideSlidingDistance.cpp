#include "twoSideSlidingDistance.h"

#include <maya/MPlug.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MVector.h>
#include <maya/MObject.h>
#include <cmath>

#include <maya/MGlobal.h>

#include <maya/MIOStream.h>

MTypeId     twoSideSlidingDistance::id( 0xc8c904 );

MObject twoSideSlidingDistance::aInputDistance1;
MObject twoSideSlidingDistance::aInputDistance2;
MObject twoSideSlidingDistance::aSliding;
MObject twoSideSlidingDistance::aDistance;
MObject twoSideSlidingDistance::aOutputDistance1;
MObject twoSideSlidingDistance::aOutputDistance2;

MObject twoSideSlidingDistance::aSlidingAttrSize;
MObject twoSideSlidingDistance::aDistanceAttrSize;

twoSideSlidingDistance::twoSideSlidingDistance() {}
twoSideSlidingDistance::~twoSideSlidingDistance() {}

MStatus twoSideSlidingDistance::initialize()
{
	MStatus stat;

	MFnNumericAttribute nAttr;

	aInputDistance1 = nAttr.create( "inputDistance1", "in1", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aInputDistance2 = nAttr.create( "inputDistance2", "in2", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	
	aSliding = nAttr.create( "sliding", "s", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aDistance = nAttr.create( "distance", "d", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	
	aOutputDistance1 = nAttr.create( "outputDistance1", "out1", MFnNumericData::kDouble, 0,0 );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aOutputDistance2 = nAttr.create( "outputDistance2", "out2", MFnNumericData::kDouble, 0,0 );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aSlidingAttrSize = nAttr.create( "slidingAttrSize", "sas", MFnNumericData::kFloat, 1 );
	nAttr.setStorable( true );
	nAttr.setMin( 0.1 );
	aDistanceAttrSize = nAttr.create( "distanceAttrSize", "das", MFnNumericData::kFloat, 1 );
	nAttr.setStorable( true );
	nAttr.setMin( 0.1 );

	stat = addAttribute( aInputDistance1 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aInputDistance2 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aSliding );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aDistance );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputDistance1 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputDistance2 );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = addAttribute( aSlidingAttrSize );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aDistanceAttrSize );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( aInputDistance1, aOutputDistance1 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInputDistance1, aOutputDistance2 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInputDistance2, aOutputDistance1 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aInputDistance2, aOutputDistance2 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aSliding, aOutputDistance1 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aSliding, aOutputDistance2 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aDistance, aOutputDistance1 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aDistance, aOutputDistance2 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	
	return MS::kSuccess;
}

MStatus twoSideSlidingDistance::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;

	if ( plug == aOutputDistance1 || plug == aOutputDistance2 )
	{
		MDataHandle hInputDistance1 = data.inputValue( aInputDistance1 );
		MDataHandle hInputDistance2 = data.inputValue( aInputDistance2 );
		MDataHandle hSliding = data.inputValue( aSliding );
		MDataHandle hDistance = data.inputValue( aDistance );
		MDataHandle hOutputDistance1 = data.outputValue( aOutputDistance1 );
		MDataHandle hOutputDistance2 = data.outputValue( aOutputDistance2 );

		MDataHandle hSlidingAttrSize = data.outputValue( aSlidingAttrSize );
		MDataHandle hDistanceAttrSize = data.outputValue( aDistanceAttrSize );

		double inputDistance1 = hInputDistance1.asDouble();
		double inputDistance2 = hInputDistance2.asDouble();

		float sas = hSlidingAttrSize.asFloat();
		float das = hDistanceAttrSize.asFloat();

		double sliding = hSliding.asDouble() / sas;
		double distance = ( 1+hDistance.asDouble()/das ) ;

		double outputDistance1 = ( 1 + sliding )*inputDistance1*distance;
		double outputDistance2 = ( 1 - sliding )*inputDistance2*distance;

		hOutputDistance1.set( outputDistance1 );
		hOutputDistance2.set( outputDistance2 );
		
		data.setClean( plug );
	}

	return MS::kSuccess;
}

void* twoSideSlidingDistance::creator()
{
	return new twoSideSlidingDistance();
}