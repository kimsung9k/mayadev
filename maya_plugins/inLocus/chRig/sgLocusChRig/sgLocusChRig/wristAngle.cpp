//
// Copyright (C) characterRigCustom
// 
// File: wristAngleNode.cpp
//
// Dependency Graph Node: wristAngle
//
// Author: Maya Plug-in Wizard 2.0
//

#include "wristAngle.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>

#include <maya/MGlobal.h>

MTypeId     wristAngle::id( 0x83001 );

MObject     wristAngle::inputAxis;
MObject     wristAngle::inputMatrix;
MObject     wristAngle::outAngle;
MObject     wristAngle::angleRate;

wristAngle::wristAngle() {}
wristAngle::~wristAngle() {}

MStatus wristAngle::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == outAngle )
	{
		MDataHandle inputAxisHandle = data.inputValue( inputAxis, &returnStatus );
		MDataHandle inputData = data.inputValue( inputMatrix, &returnStatus );
		MDataHandle hAngleRate = data.inputValue( angleRate, &returnStatus );

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node wristAngle cannot get value\n" );
		else
		{
			MMatrix inMtx = inputData.asMatrix();
			short axisNum = inputAxisHandle.asShort();
			short upAxisNum = (axisNum+1)%3;
			short otherAxisNum = ( axisNum+2 )%3;

			MMatrix unitMtx;
			MMatrix aimMtx = inMtx+unitMtx;

			MVector aimVector( aimMtx( axisNum,0),aimMtx(axisNum,1),aimMtx( axisNum,2) );
			MVector upVector( inMtx( upAxisNum,0),inMtx( upAxisNum,1),inMtx( upAxisNum,2) );
			MVector unitVector( 0,0,0 );

			if( upAxisNum == 0 )
				unitVector.x = 1;
			else if( upAxisNum == 1 )
				unitVector.y = 1;
			else
				unitVector.z = 1;
			

			double scalar = upVector*aimVector/pow( aimVector.length(),2 );
			MVector projVector = aimVector*scalar;

			MVector vtVector( upVector.x-projVector.x, upVector.y-projVector.y, upVector.z-projVector.z );

			if( axisNum == 0 )
				vtVector.x=0;
			else if( axisNum == 1 )
				vtVector.y=0;
			else
				vtVector.z=0;
			
			double result = unitVector.angle( vtVector )*hAngleRate.asDouble();

			if( vtVector[ otherAxisNum ] < 0 )
				result *= -1;

			MDataHandle outputHandle = data.outputValue( wristAngle::outAngle );
			outputHandle.set( result );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* wristAngle::creator()
{
	return new wristAngle();
}

MStatus wristAngle::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute aAttr;
	MFnEnumAttribute eAttr;
	MStatus				stat;

	inputAxis = eAttr.create( "axis", "ax", 0 );
		eAttr.addField("X-Axis", 0 );
		eAttr.addField("Y-Axis", 1 );
		eAttr.addField("Z-Axis", 2 );
		eAttr.setStorable(true);

	inputMatrix = mAttr.create( "inputMatrix", "in" );
 	mAttr.setStorable(true);

	angleRate = nAttr.create( "angleRate", "ar", MFnNumericData::kDouble, 1.0 );
	aAttr.setWritable(true);
	aAttr.setStorable(true);

	outAngle = aAttr.create( "outAngle", "oa", MFnUnitAttribute::kAngle, 0.0 );
	aAttr.setWritable(false);
	aAttr.setStorable(false);

	stat = addAttribute( inputAxis );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( angleRate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outAngle );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( inputAxis, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( angleRate, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}