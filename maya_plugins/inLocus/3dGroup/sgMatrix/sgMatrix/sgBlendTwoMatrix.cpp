//
// Copyright (C) characterRigCustom
// 
// File: sgBlendTwoMatrixNode.cpp
//
// Dependency Graph Node: sgBlendTwoMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include "sgBlendTwoMatrix.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>

#include <maya/MGlobal.h>

MTypeId     sgBlendTwoMatrix::id( 0x2014091002 );

MObject     sgBlendTwoMatrix::inMatrix1;
MObject     sgBlendTwoMatrix::inMatrix2;
MObject     sgBlendTwoMatrix::attributeBlender;
MObject     sgBlendTwoMatrix::outMatrix;
MObject     sgBlendTwoMatrix::outInvMatrix;

sgBlendTwoMatrix::sgBlendTwoMatrix() {}
sgBlendTwoMatrix::~sgBlendTwoMatrix() {}

MStatus sgBlendTwoMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == outMatrix )
	{
		MDataHandle inMatrixData1 = data.inputValue( inMatrix1, &returnStatus );
		MDataHandle inMatrixData2 = data.inputValue( inMatrix2, &returnStatus );
		MDataHandle blenderData = data.inputValue( attributeBlender, &returnStatus );

		double unitMatrixList[4][4] = { 1,0,0,0,
			                            0,1,0,0,
										0,0,1,0,
										0,0,0,1 };

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node sgBlendTwoMatrix cannot get value\n" );
		else
		{
			MMatrix inMtx1 = inMatrixData1.asMatrix();
			MMatrix inMtx2 = inMatrixData2.asMatrix();
			double blender = blenderData.asDouble();

			if( plug != inMatrix1 )
				inMtx1.get( unitMatrixList );
			if( plug != inMatrix2 )
				inMtx2.get( unitMatrixList );

			double mtx1Weight = 1.0 - blender;
			double mtx2Weight = blender;

			MMatrix result = inMtx1*mtx1Weight + inMtx2*mtx2Weight;

			MDataHandle outputHandle = data.outputValue( sgBlendTwoMatrix::outMatrix );
			outputHandle.set( result );
			MDataHandle outInvHandle = data.outputValue( sgBlendTwoMatrix::outInvMatrix );
			outInvHandle.set( result.inverse() );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* sgBlendTwoMatrix::creator()
{
	return new sgBlendTwoMatrix();
}

MStatus sgBlendTwoMatrix::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	inMatrix1 = mAttr.create( "inMatrix1", "i1" );
 	mAttr.setStorable(true);
	inMatrix2 = mAttr.create( "inMatrix2", "i2" );
 	mAttr.setStorable(true);
	attributeBlender = nAttr.create( "attributeBlender", "ab", MFnNumericData::kDouble, 0.5 );
	nAttr.setStorable(true);
	outMatrix = mAttr.create( "outMatrix", "om" );
	mAttr.setStorable(false);
	outInvMatrix = mAttr.create( "outInvMatrix", "oim" );
	mAttr.setStorable(false);

	stat = addAttribute( inMatrix1 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inMatrix2 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( attributeBlender );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = addAttribute( outMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outInvMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}


	stat = attributeAffects( inMatrix1, outMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix2, outMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( attributeBlender, outMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix1, outInvMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inMatrix2, outInvMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( attributeBlender, outInvMatrix );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}