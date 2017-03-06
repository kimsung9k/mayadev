//
// Copyright (C) characterRigCustom
// 
// File: matrixToFourByFourNode.cpp
//
// Dependency Graph Node: matrixToFourByFour
//
// Author: Maya Plug-in Wizard 2.0
//

#include "matrixToFourByFour.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>

#include <maya/MGlobal.h>

MTypeId     matrixToFourByFour::id( 0x83007 );

MObject     matrixToFourByFour::inMatrix;
MObject     matrixToFourByFour::out[4][4];

matrixToFourByFour::matrixToFourByFour() {}
matrixToFourByFour::~matrixToFourByFour() {}

bool matrixToFourByFour::allPlug( const MPlug& plug )
{
	for( int i=0; i < 4; i++ ){
		for( int  j=0; j<4; j++ ){
			if( plug == out[i][j] ) return true;
			return false;
		}
	}
}

MStatus matrixToFourByFour::compute( const MPlug& plug, MDataBlock& data )
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
			MGlobal::displayError( "Node matrixToFourByFour cannot get value\n" );
		else
		{
			MMatrix inMtx = inMatrixData.asMatrix();

			if( plug != inMatrix )
				inMtx.get( unitMatrixList );

			
			MDataHandle outHandle[4][4];

			for( int i=0; i < 4; i++ ){
				for( int  j=0; j<4; j++ ){
					MDataHandle outHandle = data.outputValue( matrixToFourByFour::out[i][j] );
					outHandle.set( inMtx( i,j ) );
				}
			}
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* matrixToFourByFour::creator()
{
	return new matrixToFourByFour();
}

MStatus matrixToFourByFour::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	inMatrix = mAttr.create( "inMatrix", "imat" );
 	mAttr.setStorable(true);

	char outputLongName[6] = "out00";
	char outputShortName[4] = "o00";

	for( int i=0; i < 4; i++ ){
		for( int  j=0; j<4; j++ ){
			outputLongName[3] = i+48;
			outputLongName[4] = j+48;
			outputShortName[1] = i+48;
			outputShortName[2] = j+48;
			out[i][j] = nAttr.create( outputLongName, outputShortName, MFnNumericData::kDouble, 1 );
			nAttr.setWritable(false);
		}
	}

	stat = addAttribute( inMatrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	
	for( int i=0; i < 4; i++ ){
		for( int  j=0; j<4; j++ ){
			stat = addAttribute( out[i][j] );
				if (!stat) { stat.perror("addAttribute"); return stat;}
		}
	}

	for( int i=0; i < 4; i++ ){
		for( int  j=0; j<4; j++ ){
			stat = attributeAffects( inMatrix, out[i][j] );
				if (!stat) { stat.perror("attributeAffects"); return stat;}
		}
	}
	return MS::kSuccess;
}