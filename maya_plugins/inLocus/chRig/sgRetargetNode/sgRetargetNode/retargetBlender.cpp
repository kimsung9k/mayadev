//
// Copyright (C) locusPsd
// 
// File: retargetBlender.cpp
//
// Dependency Graph Node: retargetBlender
//
// Author: Maya Plug-in Wizard 2.0
//

#include "retargetBlender.h"

#include <maya/MObjectArray.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrixArray.h>
#include <maya/MFloatArray.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MEulerRotation.h>
#include <maya/MArrayDataBuilder.h>

#include <maya/MGlobal.h>


using namespace std;

MTypeId     retargetBlender::id( 0xc8d203 );

MObject     retargetBlender::aInput;
	MObject     retargetBlender::aWeight;
	MObject     retargetBlender::aTransMatrix;
	MObject     retargetBlender::aOrientMatrix;
	MObject     retargetBlender::aUdAttr;

MObject     retargetBlender::aOrient;
	MObject     retargetBlender::aOrientX;
	MObject     retargetBlender::aOrientY;
	MObject     retargetBlender::aOrientZ;

MObject     retargetBlender::aOutTrans;
	MObject     retargetBlender::aOutTransX;
	MObject     retargetBlender::aOutTransY;
	MObject     retargetBlender::aOutTransZ;
MObject     retargetBlender::aOutOrient;
	MObject     retargetBlender::aOutOrientX;
	MObject     retargetBlender::aOutOrientY;
	MObject     retargetBlender::aOutOrientZ;
MObject     retargetBlender::aOutUdAttr;


retargetBlender::retargetBlender() {}
retargetBlender::~retargetBlender() {}

void* retargetBlender::creator()
{
	return new retargetBlender();
}

MStatus retargetBlender::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle  hArrInput = data.inputArrayValue( aInput, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle  hOrient = data.inputValue( aOrient, &status );

	int inputLength = hArrInput.elementCount();

	MMatrixArray matrix;
	MFloatArray weights;

	matrix.setLength( inputLength );
	weights.setLength( inputLength );

	float weightSum = 0.0f;

	MPxTransformationMatrix mpxOrientMatrix;
	mpxOrientMatrix.rotateTo( MEulerRotation( hOrient.asVector() ) );
	MMatrix orientMatrixInverse = mpxOrientMatrix.asMatrixInverse();

	MPxTransformationMatrix mpxMatrix;
	
	MMatrix transMatrix;
	MMatrix orientMatrix;

	MMatrix jointOrientMatrix;

	for( int i=0; i<inputLength; i++ )
	{
		MDataHandle hInput = hArrInput.inputValue();

		weights[i] = hInput.child( aWeight ).asFloat();

		transMatrix = hInput.child( aTransMatrix ).asMatrix();
		orientMatrix = hInput.child( aOrientMatrix ).asMatrix();

		orientMatrix *= orientMatrixInverse;

		mpxMatrix = orientMatrix;
		mpxMatrix.translateTo( MVector( transMatrix(3,0), transMatrix(3,1), transMatrix(3,2) ) );

		matrix[i] =  mpxMatrix.asMatrix();

		weightSum += weights[i];
		hArrInput.next();
	}

	MMatrix startMatrix;

	float originalWeight = 1;

	if( weightSum > 10 )
	{
		for( int i=0; i<inputLength; i++ )
		{
			weights[i] /= weightSum;
		}
		originalWeight = 0.0f;
	}
	else
	{
		for( int i=0; i<inputLength; i++ )
		{
			weights[i] /= 10.0f;
		}
		originalWeight -= weightSum/10.0f;
	}
	startMatrix *= originalWeight;

	for( int i=0; i<inputLength; i++ )
	{
		startMatrix += matrix[i]*weights[i];
	}

	MPxTransformationMatrix mpxResult( startMatrix );

	MDataHandle hOutTrans = data.outputValue( aOutTrans );
	MDataHandle hOutOrient = data.outputValue( aOutOrient );

	hOutTrans.set( mpxResult.translation() );
	hOutOrient.set( mpxResult.eulerRotation().asVector() );

	data.setClean( plug );

	return status;
}

MStatus retargetBlender::attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs )
{	
	MStatus status;

	for( int i=0; i< 2; i++ )
	{
		status = attributeAffects( affectAttr, *affectedAttrs[i] );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	return MS::kSuccess;
}

MStatus retargetBlender::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;

	
	MObject* affectedAttrs[2];
	affectedAttrs[0] = &aOutTrans;
	affectedAttrs[1] = &aOutOrient;
	
	aOutTransX = nAttr.create( "outTransX", "outTransX", MFnNumericData::kDouble, 0.0 );
	aOutTransY = nAttr.create( "outTransY", "outTransY", MFnNumericData::kDouble, 0.0 );
	aOutTransZ = nAttr.create( "outTransZ", "outTransZ", MFnNumericData::kDouble, 0.0 );
	aOutTrans = nAttr.create( "outTrans", "outTrans", aOutTransX, aOutTransY, aOutTransZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aOutTrans ) );

	aOutOrientX = uAttr.create( "outOrientX", "outOrientX", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrientY = uAttr.create( "outOrientY", "outOrientY", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrientZ = uAttr.create( "outOrientZ", "outOrientZ", MFnUnitAttribute::kAngle, 0.0 );
	aOutOrient = nAttr.create( "outOrient", "outOrient", aOutOrientX, aOutOrientY, aOutOrientZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aOutOrient ) );
	
	aInput = cAttr.create( "input", "input" );
	aWeight = nAttr.create( "weight", "weight", MFnNumericData::kFloat, 10.00f );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 10.0f );
	nAttr.setKeyable( true );
	aTransMatrix = mAttr.create( "transMatrix", "transMatrix" );
	aOrientMatrix = mAttr.create( "orientMatrix", "orientMatrix" );
	
	cAttr.addChild( aWeight );
	cAttr.addChild( aTransMatrix );
	cAttr.addChild( aOrientMatrix );

	cAttr.setStorable( true );
	cAttr.setArray( true );
	addAttribute( aInput );

	aOrientX = uAttr.create( "orientX", "orientX", MFnUnitAttribute::kAngle, 0.0 );
	aOrientY = uAttr.create( "orientY", "orientY", MFnUnitAttribute::kAngle, 0.0 );
	aOrientZ = uAttr.create( "orientZ", "orientZ", MFnUnitAttribute::kAngle, 0.0 );
	aOrient = nAttr.create( "orient", "orient", aOrientX, aOrientY, aOrientZ );

	CHECK_MSTATUS( addAttribute( aOrient ) );
	
	attributeAffectsArray( aOrient, affectedAttrs );
	attributeAffectsArray( aInput, affectedAttrs );

	return MS::kSuccess;
}