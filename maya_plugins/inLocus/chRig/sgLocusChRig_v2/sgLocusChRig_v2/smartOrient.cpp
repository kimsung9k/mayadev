//
// Copyright (C) characterRigCustom
// 
// File: smartOrientNode.cpp
//
// Dependency Graph Node: smartOrient
//
// Author: Maya Plug-in Wizard 2.0
//

#include "smartOrient.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MPxTransformationMatrix.h>

#include <maya/MGlobal.h>

#include <maya/MIOStream.h>

#define PI_Half 1.57079632679489661923

using namespace std;

MTypeId     smartOrient::id( 0xc8c726 );

MObject     smartOrient::aimAxis;
MObject     smartOrient::inputMatrix;
MObject     smartOrient::outputMatrix;
MObject		smartOrient::outAngle;
	MObject     smartOrient::outAngleX;
	MObject     smartOrient::outAngleY;
	MObject     smartOrient::outAngleZ;
MObject     smartOrient::aAngleRateFirst;
MObject     smartOrient::aAngleRateSecond;
MObject     smartOrient::aAngleRateThird;

smartOrient::smartOrient() {}
smartOrient::~smartOrient() {}

double getSeta( double vertical, double horizon ){
	if( vertical == 0 && horizon == 0 )
		return 0.0;
	else if( vertical != 0 && horizon == 0 )
		return PI_Half;
	else if( vertical == 0 && horizon != 0 )
		return 0.0;
	else
	{
		double dist = sqrt( pow( vertical,2 ) + pow( horizon, 2 ) ); 
		return acos( abs( horizon/dist ) );
	}
}

MVector verticalVector( MVector v1, MVector v2 )
{
	v1.normalize();
	v2.normalize();
	MVector projV = (v1*v2)*v2;
	return v1-projV;
}

MStatus smartOrient::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;

	MDataHandle inputData = data.inputValue( inputMatrix, &returnStatus );
	MDataHandle aimAxisData = data.inputValue( aimAxis, &returnStatus );

	if( returnStatus != MS::kSuccess )
		MGlobal::displayError( "Node smartOrient cannot get value\n" );
	else
	{
		MMatrix inMtx = inputData.asMatrix();

		short aimAxisValue = aimAxisData.asShort();
		short secondAxisValue = (aimAxisValue+1)%3;
		short thirdAxisValue = (aimAxisValue+2)%3;

		MVector aimVector( inMtx(aimAxisValue,0),inMtx(aimAxisValue,1),inMtx(aimAxisValue,2) );
		MVector upVector1;
		MVector upVector2;

		if( aimAxisValue == 0 ){
			upVector1.x =0, upVector1.y=1, upVector1.z=0;
			upVector2.x =0, upVector2.y=0, upVector2.z=1;
		}
		else if( aimAxisValue == 1 ){
			upVector1.x =0, upVector1.y=0, upVector1.z=1;
			upVector2.x =1, upVector2.y=0, upVector2.z=0;
		}
		else{
			upVector1.x =1, upVector1.y=0, upVector1.z=0;
			upVector2.x =0, upVector2.y=1, upVector2.z=0;
		}

		aimVector.normalize();

		double angle1 = acos( aimVector*upVector1 );
		double angle2 = acos( aimVector*upVector2 );

		MVector angleUpVector1;
		MVector angleUpVector2;

		if( aimAxisValue == 0 ){
			angleUpVector1.x = -cos( angle1 );
			angleUpVector2.x = -cos( angle2 );
		}
		else if( aimAxisValue == 1 ){
			angleUpVector1.y = -cos( angle1 );
			angleUpVector2.y = -cos( angle2 );
		}
		else{
			angleUpVector1.z = -cos( angle1 );
			angleUpVector2.z = -cos( angle2 );
		}


		if( aimAxisValue == 0 ){
			angleUpVector1.y = sin( angle1 );
			angleUpVector2.z = sin( angle2 );
		}
		else if( aimAxisValue == 1 ){
			angleUpVector1.z = sin( angle1 );
			angleUpVector2.x = sin( angle2 );
		}
		else{
			angleUpVector1.x = sin( angle1 );
			angleUpVector2.y = sin( angle2 );
		}
			
		double matrixList[4][4] = { 1,0,0,0,
									0,1,0,0,
									0,0,1,0,
									0,0,0,1 };

		double aimValue = inMtx( aimAxisValue, aimAxisValue );
		double vertical = inMtx(aimAxisValue,secondAxisValue);
		double horizen = inMtx(aimAxisValue,thirdAxisValue);
			
		double seta = getSeta( vertical, horizen );

		double aimR_rate = acos( aimValue )/PI_Half;

		if( aimValue > 0.99999 )
			aimR_rate = 0.0;

		float weight1 = seta/PI_Half;
		float weight2 = 1-weight1;

		MVector mAimVector( aimVector[0], aimVector[1], aimVector[2] );
		MVector mUpVector1( angleUpVector1[0], angleUpVector1[1], angleUpVector1[2] );
		MVector mUpVector2( angleUpVector2[0], angleUpVector2[1], angleUpVector2[2] );

		MVector mCrossVector = mUpVector2^mAimVector;

		MVector mAverageUpVector = mUpVector1*weight2 + mCrossVector*weight1;
		MVector mSecondVector = verticalVector( mAverageUpVector, mAimVector );
		MVector mThirdVector = mAimVector^mSecondVector;

		matrixList[aimAxisValue][0] = aimVector[0];
		matrixList[aimAxisValue][1] = aimVector[1];
		matrixList[aimAxisValue][2] = aimVector[2];

		matrixList[secondAxisValue][0] = mSecondVector.x;
		matrixList[secondAxisValue][1] = mSecondVector.y;
		matrixList[secondAxisValue][2] = mSecondVector.z;

		matrixList[thirdAxisValue][0] = mThirdVector.x;
		matrixList[thirdAxisValue][1] = mThirdVector.y;
		matrixList[thirdAxisValue][2] = mThirdVector.z;

		MMatrix outmat( matrixList );
		MPxTransformationMatrix transform( outmat );

		MVector rot = transform.eulerRotation().asVector();

		mSecondVector.normalize();

		MVector upVector( inMtx(secondAxisValue,0),inMtx(secondAxisValue,1),inMtx(secondAxisValue,2) );

		float angleFirstRate = mSecondVector.angle( upVector )/PI_Half;
		float angleSecondRate = aimR_rate*weight2;
		float angleThirdRate = aimR_rate*weight1;

		if( ( mAimVector^mSecondVector )*upVector < 0 )
			angleFirstRate *= -1;
		if( horizen < 0 )
			angleSecondRate *= -1;
		if( vertical < 0  )
			angleThirdRate *= -1;

		MDataHandle outputMatrixHandle = data.outputValue( smartOrient::outputMatrix );
		outputMatrixHandle.set( outmat );
		MDataHandle outputHandle = data.outputValue( smartOrient::outAngle );
		MDataHandle outputHandleX = outputHandle.child( outAngleX );
		outputHandleX.set( rot.x );
		MDataHandle outputHandleY = outputHandle.child( outAngleY );
		outputHandleY.set( rot.y );
		MDataHandle outputHandleZ = outputHandle.child( outAngleZ );
		outputHandleZ.set( rot.z );

		MDataHandle angleRateFirstHandle = data.outputValue( smartOrient::aAngleRateFirst );
		angleRateFirstHandle.set( angleFirstRate );
		MDataHandle angleRateSecondHandle = data.outputValue( smartOrient::aAngleRateSecond );
		angleRateSecondHandle.set( angleSecondRate );
		MDataHandle angleRateThirdHandle = data.outputValue( smartOrient::aAngleRateThird );
		angleRateThirdHandle.set( angleThirdRate );
		data.setClean(plug);
	}

	return MS::kSuccess;
}

void* smartOrient::creator()
{
	return new smartOrient();
}

MStatus smartOrient::initialize()	
{
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute aAttr;
	MFnEnumAttribute eAttr;
	MStatus				stat;

	aimAxis = eAttr.create( "aimAxis", "aim", 0 );
		eAttr.addField("X-Axis", 0 );
		eAttr.addField("Y-Axis", 1 );
		eAttr.addField("Z-Axis", 2 );
		eAttr.addField("-X-Axis", 3 );
		eAttr.addField("-Y-Axis", 4 );
		eAttr.addField("-Z-Axis", 5 );
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
	outAngle = nAttr.create( "outAngle", "oa", outAngleX, outAngleY, outAngleZ );
	nAttr.setStorable( false );
	
	aAngleRateFirst = nAttr.create( "angleRateFirst", "arf", MFnNumericData::kFloat, 0.0 );
	nAttr.setWritable(false);
	nAttr.setStorable(false);
	aAngleRateSecond = nAttr.create( "angleRateSecond", "ars", MFnNumericData::kFloat, 0.0 );
	nAttr.setWritable(false);
	nAttr.setStorable(false);
	aAngleRateThird = nAttr.create( "angleRateThird", "art", MFnNumericData::kFloat, 0.0 );
	nAttr.setWritable(false);
	nAttr.setStorable(false);

	stat = addAttribute( aimAxis );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outAngle );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aAngleRateFirst);
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aAngleRateSecond );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aAngleRateThird );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( inputMatrix, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outputMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, aAngleRateFirst);
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, aAngleRateSecond );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, aAngleRateThird );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}