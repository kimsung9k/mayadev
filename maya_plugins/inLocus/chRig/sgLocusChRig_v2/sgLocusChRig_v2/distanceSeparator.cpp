#include "distanceSeparator.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>

#include <maya/MVector.h>

MTypeId distanceSeparator::id( 0xc8c912 );

MObject  distanceSeparator::aInputDistance;
MObject  distanceSeparator::aMultMinus;
MObject  distanceSeparator::aParameter;
MObject  distanceSeparator::aSepDistance;

distanceSeparator::distanceSeparator() {};
distanceSeparator::~distanceSeparator() {};


MStatus distanceSeparator::initialize()
{
	MStatus stat;

	MFnNumericAttribute nAttr;
	
	aInputDistance = nAttr.create( "inputDistance", "id", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable( true );

	aMultMinus = nAttr.create( "multMinus", "mm", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );

	aParameter = nAttr.create( "parameter", "pr", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	
	aSepDistance = nAttr.create( "sepDistance", "sd", MFnNumericData::kDouble, 1.0 );
	nAttr.setArray( true );
	nAttr.setUsesArrayDataBuilder( true );
	nAttr.setStorable( false );

	stat = addAttribute( aInputDistance );
	if( !stat ){ stat.perror( "addAttribute : InputDistance" ); return stat; }
	stat = addAttribute( aMultMinus );
	if( !stat ){ stat.perror( "addAttribute : MultMinus" ); return stat; }
	stat = addAttribute( aParameter );
	if( !stat ){ stat.perror( "addAttribute : Parameter" ); return stat; }
	stat = addAttribute( aSepDistance );
	if( !stat ){ stat.perror( "addAttribute : SepDistance" ); return stat; }

	stat = attributeAffects( aInputDistance, aSepDistance );
	if( !stat ){ stat.perror( "attributeAffects : InputDistance" ); return stat; }
	stat = attributeAffects( aMultMinus, aSepDistance );
	if( !stat ){ stat.perror( "attributeAffects : multMinus" ); return stat; }
	stat = attributeAffects( aParameter, aSepDistance );
	if( !stat ){ stat.perror( "attributeAffects : SepDistance" ); return stat; }

	return MS::kSuccess;
}


MStatus distanceSeparator::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	if( plug == aSepDistance )
	{
		MDataHandle hInputDistance     = block.inputValue( aInputDistance );
		MDataHandle hMultMinus         = block.inputValue( aMultMinus );
		MArrayDataHandle hArrParameter = block.inputArrayValue( aParameter );

		double inputDistance = hInputDistance.asDouble();

		if( hMultMinus.asBool() )
			inputDistance *= -1;

		int elementCount = hArrParameter.elementCount();

		double* sepDistancePtr = new double[ elementCount+1 ];
		double currentParameter = 0;
		for( int i=0; i<elementCount; i++ )
		{
			MDataHandle hParameter = hArrParameter.inputValue();
			double parameter = hParameter.asDouble();
			sepDistancePtr[i] = inputDistance*( parameter - currentParameter );
			currentParameter = parameter;
			hArrParameter.next();
		}
		sepDistancePtr[elementCount] = inputDistance*( 1-currentParameter );

		MArrayDataHandle hArrSepDistance = block.outputArrayValue( aSepDistance ); 
		MArrayDataBuilder dArrSepDistance( aSepDistance, elementCount+1, &stat );

		for( int i=0; i<elementCount+1; i++ )
		{
			MDataHandle hSepDistance = dArrSepDistance.addElement( i );
			hSepDistance.set( sepDistancePtr[i] );
		}
		hArrSepDistance.set( dArrSepDistance );
		hArrSepDistance.setAllClean();

		block.setClean( plug );

		delete []sepDistancePtr;
	}

	return MS::kSuccess;
}


void* distanceSeparator::creator()
{
	return new distanceSeparator();
}