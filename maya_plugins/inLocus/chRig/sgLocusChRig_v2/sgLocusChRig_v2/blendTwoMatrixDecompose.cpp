#include "blendTwoMatrixDecompose.h"

#include <maya/MPlug.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MVector.h>
#include <maya/MObject.h>
#include <maya/MMatrix.h>
#include <maya/MPxTransformationMatrix.h>
#include <cmath>

#include <maya/MGlobal.h>

#include <maya/MIOStream.h>

MTypeId     blendTwoMatrixDecompose::id( 0xc8c907 );

MObject blendTwoMatrixDecompose::aMatrix1;
MObject blendTwoMatrixDecompose::aMatrix2;

MObject blendTwoMatrixDecompose::aBlender;

MObject blendTwoMatrixDecompose::aOutputTranslate;
	MObject blendTwoMatrixDecompose::aOutputTranslateX;
	MObject blendTwoMatrixDecompose::aOutputTranslateY;
	MObject blendTwoMatrixDecompose::aOutputTranslateZ;
MObject blendTwoMatrixDecompose::aOutputRotate;
	MObject blendTwoMatrixDecompose::aOutputRotateX;
	MObject blendTwoMatrixDecompose::aOutputRotateY;
	MObject blendTwoMatrixDecompose::aOutputRotateZ;
MObject blendTwoMatrixDecompose::aOutputScale;
	MObject blendTwoMatrixDecompose::aOutputScaleX;
	MObject blendTwoMatrixDecompose::aOutputScaleY;
	MObject blendTwoMatrixDecompose::aOutputScaleZ;
MObject blendTwoMatrixDecompose::aOutputShear;
	MObject blendTwoMatrixDecompose::aOutputShearX;
	MObject blendTwoMatrixDecompose::aOutputShearY;
	MObject blendTwoMatrixDecompose::aOutputShearZ;

blendTwoMatrixDecompose::blendTwoMatrixDecompose() {}
blendTwoMatrixDecompose::~blendTwoMatrixDecompose() {}

MStatus blendTwoMatrixDecompose::initialize()
{
	MStatus stat;

	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;

	aMatrix1 = mAttr.create( "inMatrix1", "i1" );
	mAttr.setStorable( true );
	aMatrix2 = mAttr.create( "inMatrix2", "i2" );
	mAttr.setStorable( true );
	
	aBlender = nAttr.create( "attributeBlender", "ab", MFnNumericData::kFloat, 0.5 );
	nAttr.setMin(0);
	nAttr.setMax(1);
	nAttr.setStorable( true );

	aOutputTranslateX = nAttr.create( "outputTranslateX", "otx", MFnNumericData::kDouble, 0.0 );
	aOutputTranslateY = nAttr.create( "outputTranslateY", "oty", MFnNumericData::kDouble, 0.0 );
	aOutputTranslateZ = nAttr.create( "outputTranslateZ", "otz", MFnNumericData::kDouble, 0.0 );
	aOutputTranslate = nAttr.create( "outputTranslate", "ot", aOutputTranslateX, aOutputTranslateY, aOutputTranslateZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	
	aOutputRotateX = uAttr.create( "outputRotateX", "orx", MFnUnitAttribute::kAngle, 0.0 );
	aOutputRotateY = uAttr.create( "outputRotateY", "ory", MFnUnitAttribute::kAngle, 0.0 );
	aOutputRotateZ = uAttr.create( "outputRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0 );
	aOutputRotate = nAttr.create( "outputRotate", "or", aOutputRotateX, aOutputRotateY, aOutputRotateZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	
	aOutputScaleX = nAttr.create( "outputScaleX", "osx", MFnNumericData::kDouble, 0.0 );
	aOutputScaleY = nAttr.create( "outputScaleY", "osy", MFnNumericData::kDouble, 0.0 );
	aOutputScaleZ = nAttr.create( "outputScaleZ", "osz", MFnNumericData::kDouble, 0.0 );
	aOutputScale = nAttr.create( "outputScale", "os", aOutputScaleX, aOutputScaleY, aOutputScaleZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aOutputShearX = nAttr.create( "outputShearX", "oshx", MFnNumericData::kDouble, 0.0 );
	aOutputShearY = nAttr.create( "outputShearY", "oshy", MFnNumericData::kDouble, 0.0 );
	aOutputShearZ = nAttr.create( "outputShearZ", "oshz", MFnNumericData::kDouble, 0.0 );
	aOutputShear = nAttr.create( "outputShear", "osh", aOutputShearX, aOutputShearY, aOutputShearZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	stat = addAttribute( aMatrix1 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aMatrix2 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aBlender );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputTranslate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputRotate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputScale );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputShear );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( aMatrix1, aOutputTranslate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix1, aOutputRotate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix1, aOutputScale );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix1, aOutputShear );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix2, aOutputTranslate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix2, aOutputRotate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix2, aOutputScale );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrix2, aOutputShear );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aBlender, aOutputTranslate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aBlender, aOutputRotate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aBlender, aOutputScale );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aBlender, aOutputShear );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	return MS::kSuccess;
}

MStatus blendTwoMatrixDecompose::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MDataHandle hMatrix1 = block.inputValue( aMatrix1, &stat  );
	MDataHandle hMatrix2 = block.inputValue( aMatrix2, &stat  );
	MDataHandle hBlender = block.inputValue( aBlender );

	MMatrix matrix = hMatrix1.asMatrix()*( 1-hBlender.asFloat() ) + hMatrix2.asMatrix()*hBlender.asFloat();

	MPxTransformationMatrix trMtx( matrix );

	MDataHandle hOutputTranslate = block.outputValue( aOutputTranslate );
	MDataHandle hOutputRotate = block.outputValue( aOutputRotate );
	MDataHandle hOutputScale = block.outputValue( aOutputScale );
	MDataHandle hOutputShear = block.outputValue( aOutputShear );

	MVector translate = trMtx.translation();
	hOutputTranslate.set( translate );

	MVector rotate = trMtx.eulerRotation().asVector();
	hOutputRotate.set( rotate );
	
	MVector scale = trMtx.scale();
	hOutputScale.set( scale );
	
	MVector shear = trMtx.shear();
	hOutputShear.set( shear );

	block.setClean( plug );
	
	return MS::kSuccess;
}

void* blendTwoMatrixDecompose::creator()
{
	return new blendTwoMatrixDecompose();
}