#include "followDouble.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MDoubleArray.h>

#include <maya/MGlobal.h>

MTypeId     followDouble::id( 0x83009 );

MObject     followDouble::originalDouble;
MObject     followDouble::inputDouble;
MObject     followDouble::inputWeight;
MObject     followDouble::outputDouble;

followDouble::followDouble() {}
followDouble::~followDouble() {}

MStatus followDouble::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;

	if( plug == outputDouble )
	{
		MDataHandle originalDoubleData = data.inputValue( originalDouble, &returnStatus );
		MArrayDataHandle inputDoubleArrayData = data.inputArrayValue( inputDouble, &returnStatus );
		MArrayDataHandle inputWeightArrayData = data.inputArrayValue( inputWeight, &returnStatus );

		MDoubleArray doubleValues;
		MDoubleArray weightValues;
		double AllWeightValues = 0.0;
		double originalDoubleValue = originalDoubleData.asDouble();

		for( int i=0; i< inputDoubleArrayData.elementCount(); i++ )
		{
			MDataHandle indexDoubleData = inputDoubleArrayData.inputValue( &returnStatus );
			MDataHandle indexWeightData = inputWeightArrayData.inputValue( &returnStatus );

			double indexDoubleValue = indexDoubleData.asDouble();
			double indexWeightValue = indexWeightData.asDouble();

			doubleValues.append( indexDoubleValue );
			weightValues.append( indexWeightValue );
			AllWeightValues += indexWeightValue;

			inputDoubleArrayData.next();
			inputWeightArrayData.next();
		}

		double returnDouble( 0 );

		if( AllWeightValues == 0.0 )
			returnDouble = originalDoubleValue;
		else{
			if( AllWeightValues < 10.0 ){
				returnDouble = originalDoubleValue*( 10.0-AllWeightValues )/10;
				for( unsigned int i=0; i<weightValues.length(); i++ )
					returnDouble += doubleValues[i]*weightValues[i]/10.0;
			}
			else{
				for( unsigned int i=0; i<weightValues.length(); i++ )
					returnDouble += doubleValues[i]*weightValues[i]/AllWeightValues;
			}
		}

		MDataHandle outputHandle = data.outputValue( followDouble::outputDouble );
		outputHandle.set( returnDouble );

		data.setClean(plug);
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* followDouble::creator()
{
	return new followDouble();
}

MStatus followDouble::initialize()	
{
	MFnNumericAttribute nAttr;
	MStatus				stat;

	originalDouble = nAttr.create( "originalDouble", "oi", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable(true);
	nAttr.setReadable(true);
	nAttr.setWritable(true);

	inputDouble = nAttr.create( "inputDouble", "i", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray(true);
	nAttr.setStorable(true);
	nAttr.setReadable(true);
	nAttr.setWritable(true);

	inputWeight = nAttr.create( "inputWeight", "iw", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray(true);
	nAttr.setStorable(true);
	nAttr.setReadable(true);
	nAttr.setWritable(true);

	outputDouble = nAttr.create( "outputDouble", "o", MFnNumericData::kDouble, 0.0 );
	nAttr.setReadable(true);
	nAttr.setWritable(false);
	nAttr.setStorable(false);

	stat = addAttribute( originalDouble );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputDouble );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inputWeight );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outputDouble );
	if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( originalDouble, outputDouble );
	if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputDouble, outputDouble );
	if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inputWeight, outputDouble );
	if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}