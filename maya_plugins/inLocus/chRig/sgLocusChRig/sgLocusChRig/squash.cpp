#include "squash.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

MTypeId     squash::id( 0x83003 );

MObject     squash::lengthOriginal;
MObject     squash::lengthModify;
MObject     squash::squashRate;
MObject     squash::forceValue;
MObject     squash::output;

squash::squash() {}
squash::~squash() {}

MStatus squash::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == output )
	{
		MDataHandle lengthOrigHandle = data.inputValue( lengthOriginal, &returnStatus );
		MDataHandle lengthModiHandle = data.inputValue( lengthModify, &returnStatus );
		MDataHandle rateHandle = data.inputValue( squashRate, &returnStatus );
		MDataHandle forceHandle = data.inputValue( forceValue, &returnStatus );

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node squash cannot get value\n" );
		else
		{
			double lengthOrig = lengthOrigHandle.asDouble();
			double lengthModi = lengthModiHandle.asDouble();
			double rate       = rateHandle.asDouble();
			double force      = forceHandle.asDouble();

			double result = pow( lengthOrig/lengthModi, 0.5*rate )*(1+force);

			MDataHandle outputHandle = data.outputValue( squash::output );
			outputHandle.set( result );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* squash::creator()
{
	return new squash();
}

MStatus squash::initialize()
{
	MFnNumericAttribute nAttr;
	MStatus				stat;

	lengthOriginal = nAttr.create( "lengthOriginal", "lo", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable(true);
	lengthModify = nAttr.create( "lengthModify", "lm", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable(true);
	squashRate = nAttr.create( "squashRate", "r", MFnNumericData::kDouble, 1.0 );
	nAttr.setStorable(true);
	forceValue = nAttr.create( "forceValue", "f", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable(true);

	output = nAttr.create( "output", "o", MFnNumericData::kDouble, 0.0 );
	nAttr.setWritable(false);
	nAttr.setStorable(true);

	stat = addAttribute( lengthOriginal );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( lengthModify );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( squashRate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( forceValue );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( output );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = attributeAffects( lengthOriginal, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( lengthModify, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( squashRate, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( forceValue, output );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}