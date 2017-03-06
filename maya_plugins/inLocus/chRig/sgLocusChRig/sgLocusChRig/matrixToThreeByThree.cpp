//
// Copyright (C) characterRigCustom
// 
// File: matrixToThreeByThreeNode.cpp
//
// Dependency Graph Node: matrixToThreeByThree
//
// Author: Maya Plug-in Wizard 2.0
//

#include "matrixToThreeByThree.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>

#include <maya/MGlobal.h>

MTypeId     matrixToThreeByThree::id( 0x83006 );

MObject     matrixToThreeByThree::inMatrix;
MObject     matrixToThreeByThree::out00;
MObject     matrixToThreeByThree::out01;
MObject     matrixToThreeByThree::out02;
MObject     matrixToThreeByThree::out10;
MObject     matrixToThreeByThree::out11;
MObject     matrixToThreeByThree::out12;
MObject     matrixToThreeByThree::out20;
MObject     matrixToThreeByThree::out21;
MObject     matrixToThreeByThree::out22;

matrixToThreeByThree::matrixToThreeByThree() {}
matrixToThreeByThree::~matrixToThreeByThree() {}

bool matrixToThreeByThree::allPlug( const MPlug& plug )
{
	if( plug == out00 ) return true;
	if( plug == out01 ) return true;
	if( plug == out02 ) return true;
	if( plug == out10 ) return true;
	if( plug == out11 ) return true;
	if( plug == out12 ) return true;
	if( plug == out20 ) return true;
	if( plug == out21 ) return true;
	if( plug == out22 ) return true;
	return false;
}

MStatus matrixToThreeByThree::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( allPlug( plug ) )
	{
		MDataHandle inMatrixData = data.inputValue( inMatrix, &returnStatus );

		double unitMatrixList[4][4] = { 1,0,0,0,
			                            0,1,0,0,
										0,0,1,0,
										0,0,0,1 };

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node matrixToThreeByThree cannot get value\n" );
		else
		{
			MMatrix inMtx = inMatrixData.asMatrix();

			if( plug != inMatrix )
				inMtx.get( unitMatrixList );

			MDataHandle out00Handle = data.outputValue( matrixToThreeByThree::out00 );
			out00Handle.set( inMtx( 0,0 ) );
			MDataHandle out01Handle = data.outputValue( matrixToThreeByThree::out01 );
			out01Handle.set( inMtx( 0,1 ) );
			MDataHandle out02Handle = data.outputValue( matrixToThreeByThree::out02 );
			out02Handle.set( inMtx( 0,2 ) );
			MDataHandle out10Handle = data.outputValue( matrixToThreeByThree::out10 );
			out10Handle.set( inMtx( 1,0 ) );
			MDataHandle out11Handle = data.outputValue( matrixToThreeByThree::out11 );
			out11Handle.set( inMtx( 1,1 ) );
			MDataHandle out12Handle = data.outputValue( matrixToThreeByThree::out12 );
			out12Handle.set( inMtx( 1,2 ) );
			MDataHandle out20Handle = data.outputValue( matrixToThreeByThree::out20 );
			out20Handle.set( inMtx( 2,0 ) );
			MDataHandle out21Handle = data.outputValue( matrixToThreeByThree::out21 );
			out21Handle.set( inMtx( 2,1 ) );
			MDataHandle out22Handle = data.outputValue( matrixToThreeByThree::out22 );
			out22Handle.set( inMtx( 2,2 ) );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* matrixToThreeByThree::creator()
{
	return new matrixToThreeByThree();
}

MStatus matrixToThreeByThree::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	inMatrix = mAttr.create( "inMatrix", "imat" );
 	mAttr.setStorable(true);
	out00 = nAttr.create( "out00", "o00", MFnNumericData::kDouble, 1 );
	nAttr.setWritable(false);
	out01 = nAttr.create( "out01", "o01", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out02 = nAttr.create( "out02", "o02", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out10 = nAttr.create( "out10", "o10", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out11 = nAttr.create( "out11", "o11", MFnNumericData::kDouble, 1 );
	nAttr.setWritable(false);
	out12 = nAttr.create( "out12", "o12", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out20 = nAttr.create( "out20", "o20", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out21 = nAttr.create( "out21", "o21", MFnNumericData::kDouble, 0 );
	nAttr.setWritable(false);
	out22 = nAttr.create( "out22", "o22", MFnNumericData::kDouble, 1 );
	nAttr.setWritable(false);

	stat = addAttribute( inMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = addAttribute( out00 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out01 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out02 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out10 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out11 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out12 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out20 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out21 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( out22 );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( inMatrix, out00 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out01 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out02 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out10 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out11 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out12 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out20 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out21 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix, out22 );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}