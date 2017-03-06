//
// Copyright (C) locusPsd
// 
// File: timeControl.cpp
//
// Dependency Graph Node: timeControl
//
// Author: Maya Plug-in Wizard 2.0
//

#include "timeControl.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MTime.h>

#include <maya/MGlobal.h>


using namespace std;

MTypeId     timeControl::id( 0xc8d207 );

MObject     timeControl::aInTime;
MObject     timeControl::aWeight;
MObject     timeControl::aOffset;
MObject     timeControl::aMult;
MObject     timeControl::aLimitAble;
MObject     timeControl::aMinTime;
MObject     timeControl::aMaxTime;
MObject     timeControl::aOutTime;
MObject     timeControl::aOutWeight;

timeControl::timeControl() {}
timeControl::~timeControl() {}

void* timeControl::creator()
{
	return new timeControl();
}

MStatus timeControl::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hInTime = data.inputValue( aInTime );
	MDataHandle hOffset = data.inputValue( aOffset );
	MDataHandle hMult = data.inputValue( aMult );
	MDataHandle hMinTime = data.inputValue( aMinTime );
	MDataHandle hMaxTime = data.inputValue( aMaxTime );
	MDataHandle hLimitAble = data.inputValue( aLimitAble );

	MTime inTime = hInTime.asTime();
	
	double offset = hOffset.asDouble();
	double mult = hMult.asDouble();

	double timeValue = inTime.value();
	
	if( hLimitAble.asBool() )
	{
		MTime minTime = hMinTime.asTime();
		MTime maxTime = hMaxTime.asTime();
		double minTimeValue = minTime.value();
		double maxTimeValue = maxTime.value();
		if( timeValue < minTimeValue )
			timeValue = minTimeValue;
		if( timeValue > maxTimeValue )
			timeValue = maxTimeValue;
	}

	timeValue += offset;
	timeValue *= mult;

	MTime outTime( timeValue );

	MDataHandle hOutTime = data.outputValue( aOutTime );
	hOutTime.set( outTime );

	MDataHandle hWeight = data.inputValue( aWeight );
	MDataHandle hOutWeight = data.outputValue( aOutWeight );
	hOutWeight.set( hWeight.asDouble() );

	data.setClean( plug );

	return status;
}

MStatus timeControl::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;

	aOutTime = uAttr.create( "outTime", "outTime", MFnUnitAttribute::kTime, 0.0 );
	uAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aOutTime ) );

	aOutWeight = nAttr.create( "outWeight", "outWeight", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aOutWeight ) );

	aInTime = uAttr.create( "inTime", "inTime", MFnUnitAttribute::kTime, 0.0 );
	uAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aInTime ) );
	CHECK_MSTATUS( attributeAffects( aInTime, aOutTime ) );

	aWeight = nAttr.create( "weight", "weight", MFnNumericData::kDouble, 10.0 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aWeight ) );
	CHECK_MSTATUS( attributeAffects( aWeight, aOutWeight ) );

	aOffset = nAttr.create( "offset", "offset", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aOffset ) );
	CHECK_MSTATUS( attributeAffects( aOffset, aOutTime ) );

	aMult = nAttr.create( "mult", "mult", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aMult ) );
	CHECK_MSTATUS( attributeAffects( aMult, aOutTime ) );

	aLimitAble = nAttr.create( "limitAble", "limitAble", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	nAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aLimitAble ) );
	CHECK_MSTATUS( attributeAffects( aLimitAble, aOutTime ) );

	aMinTime = uAttr.create( "minTime", "minTime", MFnUnitAttribute::kTime, 1.0 );
	uAttr.setStorable( true );
	uAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aMinTime ) );
	CHECK_MSTATUS( attributeAffects( aMinTime, aOutTime ) );

	aMaxTime = uAttr.create( "maxTime", "maxTime", MFnUnitAttribute::kTime, 20.0 );
	uAttr.setStorable( true );
	uAttr.setKeyable( true );
	CHECK_MSTATUS( addAttribute( aMaxTime ) );
	CHECK_MSTATUS( attributeAffects( aMaxTime, aOutTime ) );


	return MS::kSuccess;
}