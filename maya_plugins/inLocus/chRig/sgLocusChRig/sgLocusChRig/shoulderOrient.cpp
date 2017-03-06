//
// Copyright (C) characterRigCustom
// 
// File: shoulderOrientNode.cpp
//
// Dependency Graph Node: shoulderOrient
//
// Author: Maya Plug-in Wizard 2.0
//

#include "shoulderOrient.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MPxTransformationMatrix.h>

#include <maya/MGlobal.h>

#define PI_Half 1.57079632679489661923

MTypeId     shoulderOrient::id( 0x83002 );

MObject     shoulderOrient::aimAxis;
MObject     shoulderOrient::upAxis;
MObject     shoulderOrient::inputMatrix;
MObject     shoulderOrient::outputMatrix;
MObject     shoulderOrient::outAngleX;
MObject     shoulderOrient::outAngleY;
MObject     shoulderOrient::outAngleZ;

shoulderOrient::shoulderOrient() {}
shoulderOrient::~shoulderOrient() {}

MStatus shoulderOrient::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == outAngleX || plug == outAngleY || plug == outAngleZ )
	{
		MDataHandle inputData = data.inputValue( inputMatrix, &returnStatus );
		MDataHandle aimAxisData = data.inputValue( aimAxis, &returnStatus );
		MDataHandle upAxisData = data.inputValue( upAxis, &returnStatus );

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node shoulderOrient cannot get value\n" );
		else
		{
			MMatrix inMtx = inputData.asMatrix();

			short aimAxisValue = aimAxisData.asShort();
			short upAxisValue = upAxisData.asShort();
			short otherAxisValue = 3 - aimAxisValue - upAxisValue;

			MVector aimVector( inMtx(aimAxisValue,0),inMtx(aimAxisValue,1),inMtx(aimAxisValue,2) );
			MVector upVector;

			if( upAxisValue == 0 ){
				upVector.x = 1;
				upVector.y = 0;
				upVector.z = 0;}
			else if( upAxisValue == 1 ){
				upVector.x = 0;
				upVector.y = 1;
				upVector.z = 0;}
			else{
				upVector.x = 0;
				upVector.y = 0;
				upVector.z = 1;
			}

			aimVector.normalize();

			double angle = acos( aimVector*upVector );

			MVector angleUpVector;

			if( aimAxisValue == 0 )
				angleUpVector.x = -cos( angle );
			else if( aimAxisValue == 1 )
				angleUpVector.y = -cos( angle );
			else
				angleUpVector.z = -cos( angle );


			if( upAxisValue == 0 )
				angleUpVector.x = sin( angle );
			else if( upAxisValue == 1 )
				angleUpVector.y = sin( angle );
			else
				angleUpVector.z = sin( angle );
			
			double matrixList[4][4] = { 1,0,0,0,
										0,1,0,0,
										0,0,1,0,
										0,0,0,1 };

			matrixList[aimAxisValue][0] = aimVector[0];
			matrixList[aimAxisValue][1] = aimVector[1];
			matrixList[aimAxisValue][2] = aimVector[2];

			matrixList[upAxisValue][0] = angleUpVector[0];
			matrixList[upAxisValue][1] = angleUpVector[1];
			matrixList[upAxisValue][2] = angleUpVector[2];

			MVector mAimVector( aimVector[0], aimVector[1], aimVector[2] );
			MVector mUpVector( angleUpVector[0], angleUpVector[1], angleUpVector[2] );
			MVector mCrossVector;
			
			short axisDiff = aimAxisValue - upAxisValue;
			if( axisDiff == 2 || axisDiff == -1 )
				mCrossVector = mAimVector^mUpVector;
			else
				mCrossVector = mUpVector^mAimVector;

			matrixList[otherAxisValue][0] = mCrossVector.x;
			matrixList[otherAxisValue][1] = mCrossVector.y;
			matrixList[otherAxisValue][2] = mCrossVector.z;

			MMatrix outmat( matrixList );
			MPxTransformationMatrix transform( outmat );

			MVector rot = transform.eulerRotation().asVector();

			MDataHandle outputMatrixHandle = data.outputValue( shoulderOrient::outputMatrix );
			outputMatrixHandle.set( outmat );
			MDataHandle outputHandleX = data.outputValue( shoulderOrient::outAngleX );
			outputHandleX.set( rot.x );
			MDataHandle outputHandleY = data.outputValue( shoulderOrient::outAngleY );
			outputHandleY.set( rot.y );
			MDataHandle outputHandleZ = data.outputValue( shoulderOrient::outAngleZ );
			outputHandleZ.set( rot.z );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}
	return MS::kSuccess;
}

void* shoulderOrient::creator()
{
	return new shoulderOrient();
}

MStatus shoulderOrient::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute aAttr;
	MFnEnumAttribute eAttr;
	MStatus				stat;

	aimAxis = eAttr.create( "aimAxis", "aim", 0 );
		eAttr.addField("X-Axis", 0 );
		eAttr.addField("Y-Axis", 1 );
		eAttr.addField("Z-Axis", 2 );
		eAttr.setStorable(true);
	upAxis = eAttr.create( "upAxis", "up", 1 );
		eAttr.addField("X-Axis", 0 );
		eAttr.addField("Y-Axis", 1 );
		eAttr.addField("Z-Axis", 2 );
		eAttr.setStorable(true);

	inputMatrix = mAttr.create( "inputMatrix", "in" );
 	mAttr.setStorable(true);

	outputMatrix = mAttr.create( "outputMatrix", "o" );
	mAttr.setWritable(false);
	mAttr.setStorable(false);

	outAngleX = aAttr.create( "outAngleX", "oax", MFnUnitAttribute::kAngle, 0.0 );
	aAttr.setWritable(false);
	aAttr.setStorable(false);
	outAngleY = aAttr.create( "outAngleY", "oay", MFnUnitAttribute::kAngle, 0.0 );
	aAttr.setWritable(false);
	aAttr.setStorable(false);
	outAngleZ = aAttr.create( "outAngleZ", "oaz", MFnUnitAttribute::kAngle, 0.0 );
	aAttr.setWritable(false);
	aAttr.setStorable(false);

	stat = addAttribute( aimAxis );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( upAxis );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outAngleX );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outAngleY );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outAngleZ );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( inputMatrix, outAngleX );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outAngleY );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outAngleZ );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outputMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}