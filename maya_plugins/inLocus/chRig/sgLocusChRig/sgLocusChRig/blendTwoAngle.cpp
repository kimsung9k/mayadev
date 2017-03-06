//
// Copyright (C) characterRigCustom
// 
// File: blendTwoAngleNode.cpp
//
// Dependency Graph Node: blendTwoAngle
//
// Author: Maya Plug-in Wizard 2.0
//

#include "blendTwoAngle.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>

#include <maya/MGlobal.h>

MTypeId     blendTwoAngle::id( 0x83005 );

MObject     blendTwoAngle::inAngle1;
MObject     blendTwoAngle::inAngle2;
MObject     blendTwoAngle::attributeBlender;
MObject     blendTwoAngle::outAngle;

blendTwoAngle::blendTwoAngle() {}
blendTwoAngle::~blendTwoAngle() {}

MStatus blendTwoAngle::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == outAngle )
	{
		MDataHandle inAngleData1 = data.inputValue( inAngle1, &returnStatus );
		MDataHandle inAngleData2 = data.inputValue( inAngle2, &returnStatus );
		MDataHandle blenderData = data.inputValue( attributeBlender, &returnStatus );

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node blendTwoAngle cannot get value\n" );
		else
		{
			double angle1 = inAngleData1.asDouble();
			double angle2 = inAngleData2.asDouble();
			double blender = blenderData.asDouble();

			double angle1Weight = 1.0 - blender;
			double angle2Weight = blender;

			double result = angle1*angle1Weight + angle2*angle2Weight;

			MDataHandle outputHandle = data.outputValue( blendTwoAngle::outAngle );
			outputHandle.set( result );
			data.setClean(plug);
		}
	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* blendTwoAngle::creator()
{
	return new blendTwoAngle();
}

MStatus blendTwoAngle::initialize()	
{
	MFnUnitAttribute aAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	inAngle1 = aAttr.create( "inAngle1", "i1", MFnUnitAttribute::kAngle, 0.0 );
 	aAttr.setStorable(true);
	inAngle2 = aAttr.create( "inAngle2", "i2", MFnUnitAttribute::kAngle, 0.0 );
 	aAttr.setStorable(true);
	attributeBlender = nAttr.create( "attributeBlender", "ab", MFnNumericData::kDouble, 0.5 );
	nAttr.setStorable(true);
	outAngle = aAttr.create( "outAngle", "oa", MFnUnitAttribute::kAngle, 0.0 );
	aAttr.setWritable(false);
	aAttr.setStorable(false);

	stat = addAttribute( inAngle1 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( inAngle2 );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( attributeBlender );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	stat = addAttribute( outAngle );
		if (!stat) { stat.perror("addAttribute"); return stat;}


	stat = attributeAffects( inAngle1, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( inAngle2, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects( attributeBlender, outAngle );
		if (!stat) { stat.perror("attributeAffects"); return stat;}

	return MS::kSuccess;
}