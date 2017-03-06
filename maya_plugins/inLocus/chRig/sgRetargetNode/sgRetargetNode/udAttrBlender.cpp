//
// Copyright (C) locusPsd
// 
// File: udAttrBlender.cpp
//
// Dependency Graph Node: udAttrBlender
//
// Author: Maya Plug-in Wizard 2.0
//

#include "udAttrBlender.h"

#include <maya/MObjectArray.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MFloatArray.h>
#include <maya/MArrayDataBuilder.h>

#include <maya/MGlobal.h>


using namespace std;

MTypeId     udAttrBlender::id( 0xc8d204 );

MObject     udAttrBlender::aProcessMessage;

MObject     udAttrBlender::aInput;
	MObject     udAttrBlender::aWeight;
	MObject     udAttrBlender::aUdAttr;

MObject     udAttrBlender::aOutput;


udAttrBlender::udAttrBlender() {}
udAttrBlender::~udAttrBlender() {}

void* udAttrBlender::creator()
{
	return new udAttrBlender();
}

MStatus udAttrBlender::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle  hProcessMessage  = data.inputValue( aProcessMessage );
	bool messageOn = hProcessMessage.asBool();

	MArrayDataHandle  hArrInput = data.inputArrayValue( aInput, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	int inputLength = hArrInput.elementCount();

	float weightSum = 0.0f;

	MDoubleArray* udAttrArray = new MDoubleArray[ inputLength ];
	int udElementLen = 0;

	MFloatArray weights;
	weights.setLength( inputLength );

	for( int i=0; i<inputLength; i++ )
	{
		MDataHandle hInput = hArrInput.inputValue();

		weights[i] = hInput.child( aWeight ).asFloat();

		MArrayDataHandle hArrUdAttr = hInput.child( aUdAttr );

		udElementLen = hArrUdAttr.elementCount();

		udAttrArray[i].setLength( udElementLen );

		for( int j=0; j< udElementLen; j++ )
		{
			MDataHandle hUdAttr = hArrUdAttr.inputValue();
			udAttrArray[i][j] = hUdAttr.asDouble();
			hArrUdAttr.next();
		}
		weightSum += weights[i];
		hArrInput.next();
	}

	if( weightSum == 0 )
	{
		for( int i=0; i<inputLength; i++ )
		{
			weights[i] = 0;
		}
	}
	if( weightSum > 10 )
	{
		for( int i=0; i<inputLength; i++ )
		{
			weights[i] /= weightSum;
		}
	}
	else
	{
		for( int i=0; i<inputLength; i++ )
		{
			weights[i] /= 10.0f;
		}
	}

	MArrayDataHandle hArrOutUdAttr = data.outputArrayValue( aOutput );
	MArrayDataBuilder udAttrBullder( aOutput, udElementLen, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDoubleArray startUdAttr;
	startUdAttr.setLength( udElementLen );
	for( int j=0; j<udElementLen; j++ )
		startUdAttr[j] = 0.0;

	for( int i=0; i<inputLength; i++ )
	{
		int udAttrLength = udAttrArray[i].length();
		for( int j=0; j < udAttrLength ; j++ )
		{
			if( udElementLen <= j ) break;
			startUdAttr[j] += udAttrArray[i][j]*weights[i];
		}
	}

	for( int j=0; j < udElementLen; j++ )
	{
		MDataHandle hOutUdAttr = udAttrBullder.addElement( j );
		hOutUdAttr.set( startUdAttr[j] );
	}

	hArrOutUdAttr.set( udAttrBullder );
	hArrOutUdAttr.setAllClean();
	data.setClean( plug );

	delete []udAttrArray;

	return status;
}

MStatus udAttrBlender::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;

	aOutput = nAttr.create( "outUdAttr", "outUdAttr", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS( addAttribute( aOutput ) );

	aProcessMessage = nAttr.create( "processMessage", "processMessage", MFnNumericData::kBoolean, false );
	nAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aProcessMessage ) );
	CHECK_MSTATUS( attributeAffects( aProcessMessage, aOutput ) );
	
	aInput = cAttr.create( "input", "input" );
	cAttr.setStorable( true );
	cAttr.setArray( true );

	aUdAttr = nAttr.create( "udAttr", "udAttr", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray( true );
	aWeight = nAttr.create( "weight", "weight", MFnNumericData::kFloat, 10.00f );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 10.0f );
	
	cAttr.addChild( aUdAttr );
	cAttr.addChild( aWeight );

	CHECK_MSTATUS(  addAttribute( aInput ) );
	CHECK_MSTATUS( attributeAffects( aInput, aOutput ) );
	
	return MS::kSuccess;
}