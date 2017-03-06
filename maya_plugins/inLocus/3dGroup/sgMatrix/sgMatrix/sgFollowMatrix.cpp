#include "sgFollowMatrix.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MDoubleArray.h>

#include <maya/MGlobal.h>

MTypeId     sgFollowMatrix::id( 0x2014091003 );

MObject     sgFollowMatrix::originalMatrix;
MObject     sgFollowMatrix::inputMatrix;
MObject     sgFollowMatrix::inputWeight;
MObject     sgFollowMatrix::outputMatrix;

sgFollowMatrix::sgFollowMatrix() {}
sgFollowMatrix::~sgFollowMatrix() {}

MStatus sgFollowMatrix::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;

	if( plug == outputMatrix )
	{
		MArrayDataHandle inputMatrixArrayData = data.inputArrayValue( inputMatrix, &returnStatus );
		MArrayDataHandle inputWeightArrayData = data.inputArrayValue( inputWeight, &returnStatus );

		MMatrixArray MatrixValues;
		MDoubleArray weightValues;
		double AllWeightValues = 0;

		for( int i=0; i< inputMatrixArrayData.elementCount(); i++ )
		{
			MDataHandle indexMatrixData = inputMatrixArrayData.inputValue( &returnStatus );
			MDataHandle indexWeightData = inputWeightArrayData.inputValue( &returnStatus );

			if( !returnStatus )
				break;

			MMatrix indexMatrixValue = indexMatrixData.asMatrix();
			double indexWeightValue = indexWeightData.asDouble();

			MatrixValues.append( indexMatrixValue );
			weightValues.append( indexWeightValue/10.0 );
			AllWeightValues += indexWeightValue/10.0;

			inputMatrixArrayData.next();
			inputWeightArrayData.next();
		}

		MMatrix originalMatrixValue;

		MDataHandle originalMatrixData = data.inputValue( originalMatrix, &returnStatus );
		originalMatrixValue = originalMatrixData.asMatrix();

		double emptyArray[4][4] = {0,0,0,0,
			0,0,0,0,
			0,0,0,0,
			0,0,0,0};

		MMatrix returnMatrix( emptyArray );
		double originalWeightValue(1.0);

		if( AllWeightValues == 0.0 )
			returnMatrix = originalMatrixValue;
		else{
			if( AllWeightValues < 1.0 ){
				originalWeightValue = 1.0-AllWeightValues;
				returnMatrix = originalMatrixValue*( originalWeightValue );
				for( unsigned int i=0; i<MatrixValues.length(); i++ )
					returnMatrix += MatrixValues[i]* weightValues[i];
			}
			else{
				originalWeightValue = 0.0;
				for( unsigned int i=0; i<MatrixValues.length(); i++ )
					returnMatrix += MatrixValues[i]*( weightValues[i]/AllWeightValues );
			}
		}

		MDataHandle outputHandle = data.outputValue( sgFollowMatrix::outputMatrix );
		outputHandle.set( returnMatrix );

		data.setClean(plug);
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* sgFollowMatrix::creator()
{
	return new sgFollowMatrix();
}

MStatus sgFollowMatrix::initialize()	
{
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	originalMatrix = mAttr.create( "originalMatrix", "ormat" );
	mAttr.setStorable(true);
	mAttr.setReadable(true);
	mAttr.setWritable(true);

	inputMatrix = mAttr.create( "inputMatrix", "imat" );
	mAttr.setArray(true);
	mAttr.setStorable(true);
	mAttr.setReadable(true);
	mAttr.setWritable(true);

	inputWeight = nAttr.create( "inputWeight", "iw", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray(true);
	nAttr.setStorable(true);
	nAttr.setReadable(true);
	nAttr.setWritable(true);

	outputMatrix = mAttr.create( "outputMatrix", "omat" );
	mAttr.setWritable(false);
	mAttr.setStorable(false);

	stat = addAttribute( originalMatrix );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputMatrix );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputWeight );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outputMatrix );
	if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( originalMatrix, outputMatrix );
	if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputMatrix, outputMatrix );
	if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputWeight, outputMatrix );
	if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}