//
// Copyright (C) locusPsd
// 
// File: retargetOrientNode.cpp
//
// Dependency Graph Node: retargetOrientNode
//
// Author: Maya Plug-in Wizard 2.0
//

#include "retargetOrientNode.h"

#include <maya/MObjectArray.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MEulerRotation.h>

#include <maya/MGlobal.h>

#include <maya/MString.h>

#define RADIAN 0.0174532925199

using namespace std;

MTypeId     retargetOrientNode::id( 0xc8cc11 );

MObject    retargetOrientNode::aSourceMatrix;
MObject    retargetOrientNode::aSourceOrigMatrix;
MObject    retargetOrientNode::aSourceParentMatrix;

MObject    retargetOrientNode::aTargetOrigMatrix;
MObject    retargetOrientNode::aTargetParentMatrix;

MObject    retargetOrientNode::aLocalData;
	MObject    retargetOrientNode::aLocalMatrix;
	MObject    retargetOrientNode::aLocalInOffset;
	MObject    retargetOrientNode::aLocalOutOffset;
	MObject    retargetOrientNode::aLocalMult;

MObject    retargetOrientNode::aOrient;
	MObject    retargetOrientNode::aOrientX;
	MObject    retargetOrientNode::aOrientY;
	MObject    retargetOrientNode::aOrientZ;

MObject    retargetOrientNode::aOriginalRate;

MObject    retargetOrientNode::aOrientMatrix;

retargetOrientNode::retargetOrientNode() {}
retargetOrientNode::~retargetOrientNode() {}

void* retargetOrientNode::creator()
{
	return new retargetOrientNode();
}

MVector multEachAxis( MVector target, MVector multVector )
{
	MVector returnVector( target.x*multVector.x, target.y*multVector.y, target.z*multVector.z );
	return returnVector;
}
MVector addEachAxis( MVector& target, MVector addVector )
{
	MVector returnVector( target.x+addVector.x, target.y+addVector.y, target.z+addVector.z );
	return returnVector;
}
MVector degVectorToRadVector( MVector& degVector )
{
	MVector returnVector( degVector.x*RADIAN, degVector.y*RADIAN, degVector.z*RADIAN );
	return returnVector;
}
MMatrix rotMatrixMult( MMatrix targetMatrix, double multValue )
{
	MMatrix defaultMatrix;

	return targetMatrix*multValue + defaultMatrix*( 1-multValue );
}

MStatus retargetOrientNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hOrientMatrix = data.outputValue( aOrientMatrix, &status );
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
	MDataHandle hOrient = data.inputValue( aOrient, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hOriginalRate = data.inputValue( aOriginalRate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MMatrix sourceMatrix        = hSourceMatrix.asMatrix();
	MMatrix sourceOrigMatrix    = hSourceOrigMatrix.asMatrix();
	MMatrix sourceParentMatrix  = hSourceParentMatrix.asMatrix();
	MMatrix targetOrigMatrix    = hTargetOrigMatrix.asMatrix();
	MMatrix targetParentMatrix  = hTargetParentMatrix.asMatrix();
	MVector orient              = hOrient.asVector();
	double  originalRate  = hOriginalRate.asDouble();

	MArrayDataHandle hArrLocalData = data.inputArrayValue( aLocalData );
	unsigned int localCount = hArrLocalData.elementCount();
	
	for( unsigned int i=0; i< localCount; i++ )
	{
		MDataHandle hLocalData   = hArrLocalData.inputValue();
		MMatrix localMatrix = hLocalData.child( aLocalMatrix ).asMatrix();
		double localMult    = hLocalData.child( aLocalMult ).asDouble();
		MMatrix localInOffset = hLocalData.child( aLocalInOffset ).asMatrix();
		MMatrix localOutOffset = hLocalData.child( aLocalOutOffset ).asMatrix();

		localMatrix *= targetParentMatrix.inverse()*sourceParentMatrix;

		sourceMatrix *= localMatrix.inverse();
		sourceMatrix = rotMatrixMult( sourceMatrix, localMult );
		sourceMatrix = localInOffset*sourceMatrix*localOutOffset*localMatrix;

		hArrLocalData.next();
	}

	MPxTransformationMatrix orientMPxMtx;
	orientMPxMtx.rotateTo( orient );
	
	MMatrix sourceLocalMatrix = sourceMatrix*sourceOrigMatrix.inverse()*orientMPxMtx.asMatrixInverse();
	MMatrix targetLocalMatrix = sourceMatrix*sourceParentMatrix.inverse()*targetParentMatrix*targetOrigMatrix.inverse()*orientMPxMtx.asMatrixInverse();
	
	sourceMatrix = targetLocalMatrix*(1-originalRate ) + sourceLocalMatrix*originalRate;

	hOrientMatrix.set( sourceMatrix );
	data.setClean( plug );

	return status;
}

MStatus retargetOrientNode::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnCompoundAttribute cAttr;
	MFnUnitAttribute uAttr;

	aOrientMatrix = mAttr.create( "orientMatrix", "orientMatrix" );
	nAttr.setStorable( false );
	status = addAttribute( aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceMatrix = mAttr.create( "sourceMatrix", "sm" );
	status = addAttribute( aSourceMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceMatrix, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceOrigMatrix = mAttr.create( "sourceOrigMatrix", "som" );
	status = addAttribute( aSourceOrigMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceOrigMatrix, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aSourceParentMatrix = mAttr.create( "sourceParentMatrix", "spm" );
	status = addAttribute( aSourceParentMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aSourceParentMatrix, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aTargetOrigMatrix = mAttr.create( "targetOrigMatrix", "tom" );
	status = addAttribute( aTargetOrigMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aTargetOrigMatrix, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aTargetParentMatrix = mAttr.create( "targetParentMatrix", "tpm" );
	status = addAttribute( aTargetParentMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aTargetParentMatrix, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	
	aOrientX = uAttr.create( "orientX", "orix", MFnUnitAttribute::kAngle );
	aOrientY = uAttr.create( "orientY", "oriy", MFnUnitAttribute::kAngle );
	aOrientZ = uAttr.create( "orientZ", "oriz", MFnUnitAttribute::kAngle );
	aOrient  = nAttr.create( "orient" , "ori" , aOrientX, aOrientY, aOrientZ );
	status = addAttribute( aOrient );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aOrient, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aOriginalRate = nAttr.create( "originalRate", "origin", MFnNumericData::kDouble, 0.0, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 1.0 );
	nAttr.setStorable( true );
	status = addAttribute( aOriginalRate );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aOriginalRate, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aLocalData = cAttr.create( "localData", "ld" );
	
	aLocalMatrix = mAttr.create( "localMatrix", "lm" );

	aLocalMult = nAttr.create( "localMult", "localMult", MFnNumericData::kDouble, 1.0 );

	aLocalInOffset  = mAttr.create( "localInOffset", "localInOffset" );
	aLocalOutOffset  = mAttr.create( "localOutOffset", "localOutOffset" );
	
	cAttr.addChild( aLocalMatrix );
	cAttr.addChild( aLocalInOffset );
	cAttr.addChild( aLocalOutOffset );
	cAttr.addChild( aLocalMult );
	cAttr.setArray( true );
	cAttr.setStorable( true );
	cAttr.setKeyable( true );

	status = addAttribute( aLocalData );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffects( aLocalData, aOrientMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}