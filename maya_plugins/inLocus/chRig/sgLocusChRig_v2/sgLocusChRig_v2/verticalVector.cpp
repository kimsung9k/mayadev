#include "verticalVector.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MVector.h>

MTypeId verticalVector::id( 0xc8c910 );

MObject  verticalVector::aBaseVector;
	MObject  verticalVector::aBaseVectorX;
	MObject  verticalVector::aBaseVectorY;
	MObject  verticalVector::aBaseVectorZ;
MObject  verticalVector::aInputVector;
	MObject  verticalVector::aInputVectorX;
	MObject  verticalVector::aInputVectorY;
	MObject  verticalVector::aInputVectorZ;

MObject  verticalVector::aOutputInverse;
MObject  verticalVector::aOutputNormalize;
MObject  verticalVector::aOutputVector;
	MObject  verticalVector::aOutputVectorX;
	MObject  verticalVector::aOutputVectorY;
	MObject  verticalVector::aOutputVectorZ;

MObject  verticalVector::aCrossInverse;
MObject  verticalVector::aCrossNormalize;
MObject  verticalVector::aCrossVector;
	MObject  verticalVector::aCrossVectorX;
	MObject  verticalVector::aCrossVectorY;
	MObject  verticalVector::aCrossVectorZ;

verticalVector::verticalVector() {};
verticalVector::~verticalVector() {};

MStatus verticalVector::initialize()
{
	MStatus stat;

	MFnNumericAttribute nAttr;
	
	aBaseVectorX = nAttr.create( "baseVectorX", "bvx", MFnNumericData::kDouble, 1.0 );
	aBaseVectorY = nAttr.create( "baseVectorY", "bvy", MFnNumericData::kDouble, 0.0 );
	aBaseVectorZ = nAttr.create( "baseVectorZ", "bvz", MFnNumericData::kDouble, 0.0 );
	aBaseVector = nAttr.create( "baseVector", "bv", aBaseVectorX, aBaseVectorY, aBaseVectorZ );
	nAttr.setStorable( true );

	aInputVectorX = nAttr.create( "InputVectorX", "ivx", MFnNumericData::kDouble, 1.0 );
	aInputVectorY = nAttr.create( "InputVectorY", "ivy", MFnNumericData::kDouble, 1.0 );
	aInputVectorZ = nAttr.create( "InputVectorZ", "ivz", MFnNumericData::kDouble, 1.0 );
	aInputVector = nAttr.create( "InputVector", "iv", aInputVectorX, aInputVectorY, aInputVectorZ );
	nAttr.setStorable( true );
	
	aOutputNormalize = nAttr.create( "outputNormalize", "on", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	aOutputInverse = nAttr.create( "outputInverse", "oi", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	aCrossNormalize = nAttr.create( "crossNormalize", "cn", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	aCrossInverse = nAttr.create( "crossInverse", "ci", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );

	aOutputVectorX = nAttr.create( "outputVectorX", "ovx", MFnNumericData::kDouble, 0.0 );
	aOutputVectorY = nAttr.create( "outputVectorY", "ovy", MFnNumericData::kDouble, 0.0 );
	aOutputVectorZ = nAttr.create( "outputVectorZ", "ovz", MFnNumericData::kDouble, 1.0 );
	aOutputVector = nAttr.create( "outputVector", "ov", aOutputVectorX, aOutputVectorY, aOutputVectorZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	
	aCrossVectorX = nAttr.create( "crossVectorX", "cvx", MFnNumericData::kDouble, 0.0 );
	aCrossVectorY = nAttr.create( "crossVectorY", "cvy", MFnNumericData::kDouble, 1.0 );
	aCrossVectorZ = nAttr.create( "crossVectorZ", "cvz", MFnNumericData::kDouble, 0.0 );
	aCrossVector = nAttr.create( "crossVector", "cv", aCrossVectorX, aCrossVectorY, aCrossVectorZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	stat = addAttribute( aBaseVector );
	if( !stat ){ stat.perror( "addAttribute : baseVector" ); return stat; }
	stat = addAttribute( aInputVector );
	if( !stat ){ stat.perror( "addAttribute : inputVector" ); return stat; }

	stat = addAttribute( aOutputNormalize );
	if( !stat ){ stat.perror( "addAttribute : outputNormalize" ); return stat; }
	stat = addAttribute( aOutputInverse );
	if( !stat ){ stat.perror( "addAttribute : outputInverse" ); return stat; }
	stat = addAttribute( aCrossNormalize );
	if( !stat ){ stat.perror( "addAttribute : crossNormalize" ); return stat; }
	stat = addAttribute( aCrossInverse );
	if( !stat ){ stat.perror( "addAttribute : crossInverse" ); return stat; }

	stat = addAttribute( aOutputVector );
	if( !stat ){ stat.perror( "addAttribute : outputVector" ); return stat; }
	stat = addAttribute( aCrossVector );
	if( !stat ){ stat.perror( "addAttribute : crossVector" ); return stat; }

	stat = attributeAffects( aBaseVector, aOutputVector );
	if( !stat ){ stat.perror( "attributeAffects : normalize" ); return stat; }
	stat = attributeAffects( aInputVector, aOutputVector );
	if( !stat ){ stat.perror( "attributeAffects : reverse" ); return stat; }
	stat = attributeAffects( aOutputNormalize, aOutputVector );
	if( !stat ){ stat.perror( "attributeAffects : normalize" ); return stat; }
	stat = attributeAffects( aOutputInverse, aOutputVector );
	if( !stat ){ stat.perror( "attributeAffects : reverse" ); return stat; }
	stat = attributeAffects( aBaseVector, aCrossVector );
	if( !stat ){ stat.perror( "attributeAffects : baseVector" ); return stat; }
	stat = attributeAffects( aInputVector, aCrossVector );
	if( !stat ){ stat.perror( "attributeAffects : inputVector" ); return stat; }
	stat = attributeAffects( aCrossNormalize, aCrossVector );
	if( !stat ){ stat.perror( "attributeAffects : crossNormalize" ); return stat; }
	stat = attributeAffects( aCrossInverse, aCrossVector );
	if( !stat ){ stat.perror( "attributeAffects : crossInverse" ); return stat; }

	return MS::kSuccess;
}

MStatus verticalVector::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MDataHandle hBaseVector = block.inputValue( aBaseVector );
	MDataHandle hInputVector = block.inputValue( aInputVector );
	MDataHandle hOutputNormalize = block.inputValue( aOutputNormalize, &stat );
	MDataHandle hOutputInverse = block.inputValue( aOutputInverse, &stat );
	MDataHandle hCrossNormalize = block.inputValue( aCrossNormalize, &stat );
	MDataHandle hCrossInverse = block.inputValue( aCrossInverse, &stat );

	bool verticalNormalize = hOutputNormalize.asBool();
	bool verticalInverse = hOutputInverse.asBool();
	bool crossNormalize = hCrossNormalize.asBool();
	bool crossInverse = hCrossInverse.asBool();

	MVector baseVector = hBaseVector.asVector();
	MVector inputVector = hInputVector.asVector();

	MVector projVector = baseVector*(inputVector*baseVector)/( pow( baseVector.x,2 )+pow( baseVector.y,2 )+pow( baseVector.z,2 ) );
	MVector verticalVector = inputVector - projVector;
	MVector crossVector = baseVector^inputVector;

	if( verticalNormalize ) verticalVector.normalize();
	if( verticalInverse ) verticalVector*=-1;

	if( crossNormalize ) crossVector.normalize();
	if( crossInverse )  crossVector*=-1;

	MDataHandle hOutputVector = block.outputValue( aOutputVector );
	MDataHandle hCrossVector = block.outputValue( aCrossVector );

	hOutputVector.set( verticalVector );
	hCrossVector.set( crossVector );

	block.setClean( plug );

	return MS::kSuccess;
}

void* verticalVector::creator()
{
	return new verticalVector();
}