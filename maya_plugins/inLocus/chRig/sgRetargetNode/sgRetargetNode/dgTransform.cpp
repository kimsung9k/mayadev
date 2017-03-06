//
// Copyright (C) locusPsd
// 
// File: dgTransform.cpp
//
// Dependency Graph Node: dgTransform
//
// Author: Maya Plug-in Wizard 2.0
//

#include "dgTransform.h"

#include <maya/MObjectArray.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MEulerRotation.h>

#include <maya/MGlobal.h>


using namespace std;

MTypeId     dgTransform::id( 0xc8cc10 );

MObject     dgTransform::aTranslate;
	MObject     dgTransform::aTranslateX;
	MObject     dgTransform::aTranslateY;
	MObject     dgTransform::aTranslateZ;
MObject     dgTransform::aRotate;
	MObject     dgTransform::aRotateX;
	MObject     dgTransform::aRotateY;
	MObject     dgTransform::aRotateZ;
MObject     dgTransform::aScale;
	MObject     dgTransform::aScaleX;
	MObject     dgTransform::aScaleY;
	MObject     dgTransform::aScaleZ;
MObject     dgTransform::aShear;
	MObject     dgTransform::aShearX;
	MObject     dgTransform::aShearY;
	MObject     dgTransform::aShearZ;
MObject     dgTransform::aJointOrient;
	MObject     dgTransform::aJointOrientX;
	MObject     dgTransform::aJointOrientY;
	MObject     dgTransform::aJointOrientZ;

MObject     dgTransform::aInputTranslate;
	MObject     dgTransform::aInputTranslateX;
	MObject     dgTransform::aInputTranslateY;
	MObject     dgTransform::aInputTranslateZ;
MObject     dgTransform::aInputRotate;
	MObject     dgTransform::aInputRotateX;
	MObject     dgTransform::aInputRotateY;
	MObject     dgTransform::aInputRotateZ;
MObject     dgTransform::aInputScale;
	MObject     dgTransform::aInputScaleX;
	MObject     dgTransform::aInputScaleY;
	MObject     dgTransform::aInputScaleZ;
MObject     dgTransform::aInputShear;
	MObject     dgTransform::aInputShearX;
	MObject     dgTransform::aInputShearY;
	MObject     dgTransform::aInputShearZ;

MObject     dgTransform::aMatrix;
MObject     dgTransform::aInverseMatrix;
MObject     dgTransform::aWorldMatrix;
MObject     dgTransform::aWorldInverseMatrix;
MObject     dgTransform::aParentMatrix;
MObject     dgTransform::aParentInverseMatrix;

dgTransform::dgTransform() {}
dgTransform::~dgTransform() {}

void* dgTransform::creator()
{
	return new dgTransform();
}

MStatus dgTransform::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hTranslate = data.inputValue( aTranslate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hRotate    = data.inputValue( aRotate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hScale     = data.inputValue( aScale, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hShear     = data.inputValue( aShear, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hJointOrient     = data.inputValue( aJointOrient, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDataHandle hInputTranslate = data.inputValue( aInputTranslate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputRotate    = data.inputValue( aInputRotate, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputScale     = data.inputValue( aInputScale, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MDataHandle hInputShear     = data.inputValue( aInputShear, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );


	MPxTransformationMatrix inputMpxTrMtx;
	MEulerRotation inputEulerRot( hInputRotate.asVector() );

	inputMpxTrMtx.translateTo( hInputTranslate.asVector() );
	inputMpxTrMtx.rotateTo( inputEulerRot );
	inputMpxTrMtx.scaleTo( hInputScale.asVector() );
	inputMpxTrMtx.shearTo( hInputShear.asVector() );


	MMatrix parentMatrix = inputMpxTrMtx.asMatrix();


	MPxTransformationMatrix mpxTrMtx;
	MEulerRotation eulerRot( hRotate.asVector() );
	MEulerRotation joEulerRot( hJointOrient.asVector() );

	mpxTrMtx.translateTo( hTranslate.asVector() );
	mpxTrMtx.rotateTo( eulerRot );
	mpxTrMtx.rotateBy( joEulerRot );
	mpxTrMtx.scaleTo( hScale.asVector() );
	mpxTrMtx.shearTo( hShear.asVector() );

	if( plug == aMatrix )
	{
		//cout <<"matrix"<<endl;
		MDataHandle hMatrix = data.outputValue( aMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		hMatrix.setMMatrix( mpxTrMtx.asMatrix() );
	}

	if( plug == aInverseMatrix )
	{
		//cout <<"inverseMatrix"<<endl;
		MDataHandle hInverseMatrix = data.outputValue( aInverseMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		hInverseMatrix.setMMatrix( mpxTrMtx.asMatrix().inverse() );
	}

	if( plug == aWorldMatrix || plug == aWorldInverseMatrix )
	{
		MMatrix worldMatrix = mpxTrMtx.asMatrix()*parentMatrix;
		if( plug == aWorldMatrix )
		{
			//cout <<"worldMatrix"<<endl;
			MDataHandle hWorldMatrix = data.outputValue( aWorldMatrix, &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );
			hWorldMatrix.setMMatrix( worldMatrix );
		}

		if( plug == aWorldInverseMatrix )
		{
			//cout <<"worldInverseMatrix"<<endl;
			MDataHandle hWorldInverseMatrix = data.outputValue( aWorldInverseMatrix, &status );
			CHECK_MSTATUS_AND_RETURN_IT( status );
			hWorldInverseMatrix.setMMatrix( worldMatrix.inverse() );
		}
	}

	if( plug == aParentMatrix )
	{
		//cout <<"parentMatrix"<<endl;
		MDataHandle hParentMatrix = data.outputValue( aParentMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		hParentMatrix.setMMatrix( parentMatrix );
	}

	if( plug == aParentInverseMatrix )
	{
		//cout <<"parentInverseMatrix"<<endl;
		MDataHandle hParentInverseMatrix = data.outputValue( aParentInverseMatrix, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		hParentInverseMatrix.setMMatrix( parentMatrix.inverse() );
	}

	data.setClean( plug );

	return status;
}


MStatus dgTransform::attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs )
{	
	MStatus status;

	for( int i=0; i< 6; i++ )
	{
		status = attributeAffects( affectAttr, *affectedAttrs[i] );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	return MS::kSuccess;
}

MStatus dgTransform::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;

	aTranslateX = nAttr.create( "translateX", "tx", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aTranslateY = nAttr.create( "translateY", "ty", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aTranslateZ = nAttr.create( "translateZ", "tz", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aTranslate  = nAttr.create( "translate", "t", aTranslateX, aTranslateY, aTranslateZ );
	nAttr.setStorable( true );
	status = addAttribute( aTranslate );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aRotateX = uAttr.create( "rotateX", "rx", MFnUnitAttribute::kAngle, 0.0 ); uAttr.setKeyable( true );
	aRotateY = uAttr.create( "rotateY", "ry", MFnUnitAttribute::kAngle, 0.0 ); uAttr.setKeyable( true );
	aRotateZ = uAttr.create( "rotateZ", "rz", MFnUnitAttribute::kAngle, 0.0 ); uAttr.setKeyable( true );
	aRotate  = nAttr.create( "rotate", "r", aRotateX, aRotateY, aRotateZ );
	nAttr.setStorable( true );
	status = addAttribute( aRotate );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aScaleX = nAttr.create( "scaleX", "sx", MFnNumericData::kDouble, 0.0 ); nAttr.setKeyable( true );
	aScaleY = nAttr.create( "scaleY", "sy", MFnNumericData::kDouble, 0.0 ); nAttr.setKeyable( true );
	aScaleZ = nAttr.create( "scaleZ", "sz", MFnNumericData::kDouble, 0.0 ); nAttr.setKeyable( true );
	aScale  = nAttr.create( "scale", "s", aScaleX, aScaleY, aScaleZ );
	nAttr.setStorable( true );
	status = addAttribute( aScale );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aShearX = nAttr.create( "shearX", "shx", MFnNumericData::kDouble, 0.0 );
	aShearY = nAttr.create( "shearY", "shy", MFnNumericData::kDouble, 0.0 );
	aShearZ = nAttr.create( "shearZ", "shz", MFnNumericData::kDouble, 0.0 );
	aShear  = nAttr.create( "shear", "sh", aShearX, aShearY, aShearZ );
	nAttr.setStorable( true );
	status = addAttribute( aShear );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aJointOrientX = uAttr.create( "jointOrientX", "jox", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aJointOrientY = uAttr.create( "jointOrientY", "joy", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aJointOrientZ = uAttr.create( "jointOrientZ", "joz", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aJointOrient  = nAttr.create( "jointOrient", "jo", aJointOrientX, aJointOrientY, aJointOrientZ );
	nAttr.setStorable( true );
	status = addAttribute( aJointOrient );
	CHECK_MSTATUS_AND_RETURN_IT( status );


	aInputTranslateX = nAttr.create( "inputTranslateX", "itx", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputTranslateY = nAttr.create( "inputTranslateY", "ity", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputTranslateZ = nAttr.create( "inputTranslateZ", "itz", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputTranslate  = nAttr.create( "inputTranslate", "it", aInputTranslateX, aInputTranslateY, aInputTranslateZ );
	nAttr.setStorable( true );
	status = addAttribute( aInputTranslate );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aInputRotateX = uAttr.create( "inputRotateX", "irx", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aInputRotateY = uAttr.create( "inputRotateY", "iry", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aInputRotateZ = uAttr.create( "inputRotateZ", "irz", MFnUnitAttribute::kAngle, 0.0 );uAttr.setKeyable( true );
	aInputRotate  = nAttr.create( "inputRotate", "ir", aInputRotateX, aInputRotateY, aInputRotateZ );
	nAttr.setStorable( true );
	status = addAttribute( aInputRotate );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aInputScaleX = nAttr.create( "inputScaleX", "isx", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputScaleY = nAttr.create( "inputScaleY", "isy", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputScaleZ = nAttr.create( "inputScaleZ", "isz", MFnNumericData::kDouble, 0.0 );nAttr.setKeyable( true );
	aInputScale  = nAttr.create( "inputScale", "is", aInputScaleX, aInputScaleY, aInputScaleZ );
	nAttr.setStorable( true );
	status = addAttribute( aInputScale );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	aInputShearX = nAttr.create( "inputShearX", "ishx", MFnNumericData::kDouble, 0.0 );
	aInputShearY = nAttr.create( "inputShearY", "ishy", MFnNumericData::kDouble, 0.0 );
	aInputShearZ = nAttr.create( "inputShearZ", "ishz", MFnNumericData::kDouble, 0.0 );
	aInputShear  = nAttr.create( "inputShear", "ish", aInputShearX, aInputShearY, aInputShearZ );
	nAttr.setStorable( true );
	status = addAttribute( aInputShear );
	CHECK_MSTATUS_AND_RETURN_IT( status );


	MObject* affectedAttrs[6];

	aMatrix = mAttr.create( "matrix", "m" );
	nAttr.setStorable( false );
	status = addAttribute( aMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[0] = &aMatrix;

	aInverseMatrix = mAttr.create( "inverseMatrix", "im" );
	nAttr.setStorable( false );
	status = addAttribute( aInverseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[1] = &aInverseMatrix;

	aWorldMatrix = mAttr.create( "worldMatrix", "wm" );
	nAttr.setStorable( false );
	status = addAttribute( aWorldMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[2] = &aWorldMatrix;

	aWorldInverseMatrix = mAttr.create( "worldInverseMatrix", "wim" );
	nAttr.setStorable( false );
	status = addAttribute( aWorldInverseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[3] = &aWorldInverseMatrix;

	aParentMatrix = mAttr.create( "parentMatrix", "pm" );
	nAttr.setStorable( false );
	status = addAttribute( aParentMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[4] = &aParentMatrix;

	aParentInverseMatrix = mAttr.create( "parentInverseMatrix", "pim" );
	nAttr.setStorable( false );
	status = addAttribute( aParentInverseMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	affectedAttrs[5] = &aParentInverseMatrix;

	status = attributeAffectsArray( aTranslate, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aRotate, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aScale, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aShear, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aJointOrient, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aInputTranslate, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aInputRotate, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aInputScale, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = attributeAffectsArray( aInputShear, affectedAttrs );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}