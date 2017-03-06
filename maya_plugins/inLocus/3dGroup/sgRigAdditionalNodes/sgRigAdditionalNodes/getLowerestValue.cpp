#include "getLowerestValue.h"

MTypeId     getLowerestValue::id( 0x2014042700 );

MObject     getLowerestValue::aInputValue;
MObject     getLowerestValue::aOutputValue; 

getLowerestValue::getLowerestValue(){}
getLowerestValue::~getLowerestValue(){}


void* getLowerestValue::creator()
{
	return new getLowerestValue();
}


MStatus getLowerestValue::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrInputValue = data.inputArrayValue( aInputValue );

	double lowerValue = 1000000.0;
	for( unsigned int i=0; i< hArrInputValue.elementCount(); i++, hArrInputValue.next() )
	{
		double value = hArrInputValue.inputValue().asDouble();
		if( value < lowerValue )
		{
			lowerValue = value;
		}
	}

	MDataHandle hOutputValue = data.outputValue( aOutputValue );
	hOutputValue.set( lowerValue );

	data.setClean( plug );

	return MS::kSuccess;
}


MStatus getLowerestValue::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;

	aOutputValue = nAttr.create( "outputValue", "outputValue", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputValue ) );

	aInputValue = nAttr.create( "inputValue", "inputValue", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	nAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputValue ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputValue, aOutputValue ) );

	return MS::kSuccess;
}