#include "multMatrixDecompose.h"

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

MTypeId     multMatrixDecompose::id( 0xc8c905 );

MObject multMatrixDecompose::aMatrixIn;

MObject multMatrixDecompose::aInverseTranslate;
MObject multMatrixDecompose::aInverseDistance;

MObject multMatrixDecompose::aOutputTranslate;
	MObject multMatrixDecompose::aOutputTranslateX;
	MObject multMatrixDecompose::aOutputTranslateY;
	MObject multMatrixDecompose::aOutputTranslateZ;
MObject multMatrixDecompose::aOutputRotate;
	MObject multMatrixDecompose::aOutputRotateX;
	MObject multMatrixDecompose::aOutputRotateY;
	MObject multMatrixDecompose::aOutputRotateZ;
MObject multMatrixDecompose::aOutputScale;
	MObject multMatrixDecompose::aOutputScaleX;
	MObject multMatrixDecompose::aOutputScaleY;
	MObject multMatrixDecompose::aOutputScaleZ;
MObject multMatrixDecompose::aOutputShear;
	MObject multMatrixDecompose::aOutputShearX;
	MObject multMatrixDecompose::aOutputShearY;
	MObject multMatrixDecompose::aOutputShearZ;

MObject multMatrixDecompose::aOutputMatrix;
MObject multMatrixDecompose::aOutputInverseMatrix;

MObject multMatrixDecompose::aOutputDistance;

multMatrixDecompose::multMatrixDecompose()
{
	m_isDirty = true;
}
multMatrixDecompose::~multMatrixDecompose() {}

MStatus multMatrixDecompose::initialize()
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

	aOutputMatrix = mAttr.create( "outputMatrix", "om");
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	aOutputInverseMatrix = mAttr.create( "outputInverseMatrix", "oim");
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aOutputDistance = nAttr.create( "outputDistance", "od", MFnNumericData::kDouble, 0.0 );
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
	stat = addAttribute( aOutputMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputInverseMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( aOutputDistance );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( aMatrixIn, aOutputTranslate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputRotate );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputScale );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputShear );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputInverseMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( aMatrixIn, aOutputDistance );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	
	return MS::kSuccess;
}


MStatus multMatrixDecompose::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	m_isDirty = true;
	return MS::kSuccess;
}

MStatus multMatrixDecompose::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	if( m_isDirty )
	{
		MArrayDataHandle hArrMatrixIn = block.inputArrayValue( aMatrixIn );
		MDataHandle hInverseTranslate = block.inputValue( aInverseTranslate );
		MDataHandle hInverseDistance = block.inputValue( aInverseDistance );
		MDataHandle hMatrixIn= hArrMatrixIn.inputValue( &stat );
		if( !stat ){ stat.perror("matrixIn"); return stat;}

		m_bInverseTrans = hInverseTranslate.asBool();
		m_bInverseDist  = hInverseDistance.asBool();

		m_multMtx = hMatrixIn.asMatrix();
		hArrMatrixIn.next();

		for( int i=1; i<hArrMatrixIn.elementCount(); i++ )
		{
			MDataHandle hMatrixIn = hArrMatrixIn.inputValue( &stat );
			m_multMtx *= hMatrixIn.asMatrix();
			hArrMatrixIn.next();
		}	
	}

	MPxTransformationMatrix trMtx( m_multMtx );
	
	if( plug == aOutputMatrix )
	{
		MDataHandle hOutputMatrix = block.outputValue( aOutputMatrix );
		hOutputMatrix.set( m_multMtx );
	}

	if( plug == aOutputInverseMatrix )
	{
		MDataHandle hOutputInverseMatrix = block.outputValue( aOutputInverseMatrix );
		hOutputInverseMatrix.set( m_multMtx.inverse() );
	}

	if( plug == aOutputTranslate  || plug == aOutputTranslateX ||
		plug == aOutputTranslateY || plug == aOutputTranslateZ || plug == aOutputDistance )
	{
		MDataHandle hOutputTranslate = block.outputValue( aOutputTranslate );
		MDataHandle hOutputDistance = block.outputValue( aOutputDistance );

		MVector translate = trMtx.translation();

		double inverseTranslateValue = 1-2*m_bInverseTrans;
		double inverseDistanceValue =  1-2*m_bInverseDist;

		hOutputTranslate.set( translate*inverseTranslateValue );
		hOutputDistance.set( translate.length() * inverseDistanceValue );
	}
	
	if( plug == aOutputRotate  || plug == aOutputRotateX ||
		plug == aOutputRotateY || plug ==aOutputRotateZ )
	{
		MDataHandle hOutputRotate = block.outputValue( aOutputRotate );
		MVector rotate = trMtx.eulerRotation().asVector();
		hOutputRotate.set( rotate );
	}

	if( plug == aOutputScale  || plug == aOutputScaleX ||
		plug == aOutputScaleY || plug == aOutputScaleZ )
	{
		MDataHandle hOutputScale = block.outputValue( aOutputScale );
		MVector scale = trMtx.scale();
		hOutputScale.set( scale );
	}
	
	if( plug == aOutputShear  || plug == aOutputShearX ||
		plug == aOutputShearY || plug == aOutputShearZ )
	{
		MDataHandle hOutputShear = block.outputValue( aOutputShear );
		MVector shear = trMtx.shear();
		hOutputShear.set( shear );
	}

	block.setClean( plug );
	m_isDirty = false;
	
	return MS::kSuccess;
}

void* multMatrixDecompose::creator()
{
	return new multMatrixDecompose();
}