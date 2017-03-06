//
// Copyright (C) locusPsd
// 
// File: retargetTransNode.cpp
//
// Dependency Graph Node: retargetTransNode
//
// Author: Maya Plug-in Wizard 2.0
//

#include "retargetTransNode.h"

#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MFnNurbsCurve.h>

#include <maya/MGlobal.h>

#include <maya/MString.h>

using namespace std;

MTypeId     retargetTransNode::id( 0xc8cc12 );

MObject    retargetTransNode::aSourceMatrix;
MObject    retargetTransNode::aSourceOrigMatrix;
MObject    retargetTransNode::aSourceParentMatrix;

MObject    retargetTransNode::aTargetOrigMatrix;
MObject    retargetTransNode::aTargetParentMatrix;

MObject    retargetTransNode::aDistanceRate;

MObject    retargetTransNode::aLocalData;
	MObject    retargetTransNode::aLocalMatrix;

	MObject    retargetTransNode::aLocalOffset;

	MObject    retargetTransNode::aLocalMult;
		MObject    retargetTransNode::aLocalMultX;
		MObject    retargetTransNode::aLocalMultY;
		MObject    retargetTransNode::aLocalMultZ;

MObject    retargetTransNode::aOriginalRate;

MObject    retargetTransNode::aTransMatrix;

retargetTransNode::retargetTransNode() {}
retargetTransNode::~retargetTransNode() {}

void* retargetTransNode::creator()
{
	return new retargetTransNode();
}

void multEachAxis( MPoint& target, MVector multVector )
{
	target.x *= multVector.x;
	target.y *= multVector.y;
	target.z *= multVector.z;
}
void multEachAxis( MVector& target, MVector multVector )
{
	target.x *= multVector.x;
	target.y *= multVector.y;
	target.z *= multVector.z;
}
void addEachAxis( MPoint& target, MVector addVector )
{
	target.x += addVector.x;
	target.y += addVector.y;
	target.z += addVector.z;
}
void addEachAxis( MVector& target, MVector addVector )
{
	target.x += addVector.x;
	target.y += addVector.y;
	target.z += addVector.z;
}

MStatus retargetTransNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hTransMatrix = data.outputValue( aTransMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hSourceMatrix = data.inputValue( aSourceMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hSourceOrigMatrix = data.inputValue( aSourceOrigMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hSourceParentMatrix = data.inputValue( aSourceParentMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hTargetOrigMatrix = data.inputValue( aTargetOrigMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hTargetParentMatrix = data.inputValue( aTargetParentMatrix, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hDistanceRate = data.inputValue( aDistanceRate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hOriginalRate = data.inputValue( aOriginalRate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix sourceMatrix        = hSourceMatrix.asMatrix();
	MMatrix sourceOrigMatrix    = hSourceOrigMatrix.asMatrix();
	MMatrix sourceParentMatrix  = hSourceParentMatrix.asMatrix();
	MMatrix targetOrigMatrix    = hTargetOrigMatrix.asMatrix();
	MMatrix targetParentMatrix  = hTargetParentMatrix.asMatrix();
	double  distRate      = hDistanceRate.asDouble();
	double  originalRate  = hOriginalRate.asDouble();

	///////////////////////////----- Default Translate ------//////////////////////////////

	MMatrix sourceLocalCuMatrix = sourceMatrix*sourceParentMatrix.inverse();
	MMatrix sourceLocalOrigMatrix = sourceOrigMatrix*sourceParentMatrix.inverse();

	MVector sourceCuTrans( sourceLocalCuMatrix(3,0), sourceLocalCuMatrix(3,1), sourceLocalCuMatrix(3,2) );
	MVector sourceLocalOrigTrans( sourceLocalOrigMatrix(3,0), sourceLocalOrigMatrix(3,1), sourceLocalOrigMatrix(3,2) );

	MVector sourceTransVector = sourceCuTrans-sourceLocalOrigTrans;

	MMatrix targetLocalOrigMatrix = targetOrigMatrix*targetParentMatrix.inverse();
	MVector targetLocaOrigTrans( targetLocalOrigMatrix(3,0), targetLocalOrigMatrix(3,1), targetLocalOrigMatrix(3,2) );

	MPoint localTrans = ( sourceTransVector + sourceLocalOrigTrans*(1-originalRate) )*distRate + targetLocaOrigTrans*originalRate;
	MPoint outputTrans = localTrans*targetParentMatrix;

	///////////////////////////----- Default Translate End ------//////////////////////////////
	
	MArrayDataHandle hArrLocalData = data.inputArrayValue( aLocalData );
	unsigned int localCount = hArrLocalData.elementCount();

	for( unsigned int i=0; i< localCount; i++ )
	{
		MDataHandle hLocalData = hArrLocalData.inputValue();

		MMatrix localMatrix    = hLocalData.child( aLocalMatrix ).asMatrix();
		MMatrix localOffset    = hLocalData.child( aLocalOffset ).asMatrix();
		MVector localMult      = hLocalData.child( aLocalMult ).asVector();
		
		outputTrans *= localMatrix.inverse();
		multEachAxis( outputTrans, localMult );
		outputTrans *= localOffset;
		outputTrans *= localMatrix;

		hArrLocalData.next();
	}

	outputTrans *= targetOrigMatrix.inverse();

	MPxTransformationMatrix mpxTransMatrix;
	mpxTransMatrix.translateTo( outputTrans );

	hTransMatrix.set( mpxTransMatrix.asMatrix() );
	data.setClean( plug );

	return status;
}

MStatus retargetTransNode::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnCompoundAttribute cAttr;
	MFnUnitAttribute uAttr;

	aTransMatrix = mAttr.create( "transMatrix", "transMatrix" );
	nAttr.setStorable( false );
	status = addAttribute( aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceMatrix = mAttr.create( "sourceMatrix", "sm" );
	mAttr.setStorable( true );
	status = addAttribute( aSourceMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceMatrix, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceOrigMatrix = mAttr.create( "sourceOrigMatrix", "som" );
	mAttr.setStorable( true );
	status = addAttribute( aSourceOrigMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceOrigMatrix, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceParentMatrix = mAttr.create( "sourceParentMatrix", "spm" );
	mAttr.setStorable( true );
	status = addAttribute( aSourceParentMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceParentMatrix, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aTargetOrigMatrix = mAttr.create( "targetOrigMatrix", "tom" );
	mAttr.setStorable( true );
	status = addAttribute( aTargetOrigMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aTargetOrigMatrix, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aTargetParentMatrix = mAttr.create( "targetParentMatrix", "tpm" );
	mAttr.setStorable( true );
	status = addAttribute( aTargetParentMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aTargetParentMatrix, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aDistanceRate = nAttr.create( "distanceRate", "distr", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable( true );
	status = addAttribute( aDistanceRate );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aDistanceRate, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aOriginalRate = nAttr.create( "originalRate", "origin", MFnNumericData::kDouble, 0.0, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setStorable( true );
	status = addAttribute( aOriginalRate );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aOriginalRate, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aLocalData = cAttr.create( "localData", "ld" );
	
	aLocalMatrix = mAttr.create( "localMatrix", "lm" );

	aLocalMultX = nAttr.create( "localMultX", "lmx", MFnNumericData::kDouble, 1.0 );
	aLocalMultY = nAttr.create( "localMultY", "lmy", MFnNumericData::kDouble, 1.0 );
	aLocalMultZ = nAttr.create( "localMultZ", "lmz", MFnNumericData::kDouble, 1.0 );
	aLocalMult  = nAttr.create( "localMult", "lmult", aLocalMultX, aLocalMultY, aLocalMultZ );

	aLocalOffset = mAttr.create( "localOffset", "localOffset" );
	
	cAttr.addChild( aLocalMatrix );
	cAttr.addChild( aLocalMult );
	cAttr.addChild( aLocalOffset );
	cAttr.setArray( true );
	cAttr.setStorable( true );

	status = addAttribute( aLocalData );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aLocalData, aTransMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}