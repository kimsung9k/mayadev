#include "sgMultMatrixDecompose.h"

#include <maya/MPlug.h>
#include <maya/MStatus.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MVector.h>
#include <maya/MObject.h>
#include <maya/MMatrix.h>
#include <maya/MPxTransformationMatrix.h>

#include <maya/MGlobal.h>

MTypeId     sgMultMatrixDecompose::id( 0x2014091001 );

MObject sgMultMatrixDecompose::aMatrixIn;

MObject sgMultMatrixDecompose::aInverseTranslate;
MObject sgMultMatrixDecompose::aInverseDistance;

MObject sgMultMatrixDecompose::aOutputTranslate;
	MObject sgMultMatrixDecompose::aOutputTranslateX;
	MObject sgMultMatrixDecompose::aOutputTranslateY;
	MObject sgMultMatrixDecompose::aOutputTranslateZ;
MObject sgMultMatrixDecompose::aOutputRotate;
	MObject sgMultMatrixDecompose::aOutputRotateX;
	MObject sgMultMatrixDecompose::aOutputRotateY;
	MObject sgMultMatrixDecompose::aOutputRotateZ;
MObject sgMultMatrixDecompose::aOutputScale;
	MObject sgMultMatrixDecompose::aOutputScaleX;
	MObject sgMultMatrixDecompose::aOutputScaleY;
	MObject sgMultMatrixDecompose::aOutputScaleZ;
MObject sgMultMatrixDecompose::aOutputShear;
	MObject sgMultMatrixDecompose::aOutputShearX;
	MObject sgMultMatrixDecompose::aOutputShearY;
	MObject sgMultMatrixDecompose::aOutputShearZ;

sgMultMatrixDecompose::sgMultMatrixDecompose() {}
sgMultMatrixDecompose::~sgMultMatrixDecompose() {}

MStatus sgMultMatrixDecompose::initialize()
{
	MStatus stat;

	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;

	aMatrixIn = mAttr.create( "matrixIn", "i" );
	mAttr.setArray( true );
	mAttr.setUsesArrayDataBuilder( true );
	mAttr.setStorable( true );

	aInverseTranslate = nAttr.create( "inverseTranslate", "invt", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	aInverseDistance = nAttr.create( "inverseDistance", "invd", MFnNumericData::kBoolean, false );
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

	stat = addAttribute( aMatrixIn );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aInverseTranslate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aInverseDistance );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputTranslate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputRotate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputScale );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputShear );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( aMatrixIn, aOutputTranslate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputRotate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputScale );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputShear );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	
	return MS::kSuccess;
}

MStatus sgMultMatrixDecompose::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MArrayDataHandle hArrMatrixIn = block.inputArrayValue( aMatrixIn );
	MDataHandle hInverseTranslate = block.inputValue( aInverseTranslate );
	MDataHandle hInverseDistance = block.inputValue( aInverseDistance );
	MDataHandle hMatrixIn= hArrMatrixIn.inputValue( &stat );
	if( !stat ){ stat.perror("matrixIn"); return stat;}

	MMatrix multMtx = hMatrixIn.asMatrix();
	hArrMatrixIn.next();

	for( int i=1; i<hArrMatrixIn.elementCount(); i++ )
	{
		MDataHandle hMatrixIn = hArrMatrixIn.inputValue( &stat );
		multMtx *= hMatrixIn.asMatrix();
		hArrMatrixIn.next();
	}

	MPxTransformationMatrix trMtx( multMtx );
	
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

void* sgMultMatrixDecompose::creator()
{
	return new sgMultMatrixDecompose();
}