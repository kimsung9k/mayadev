//
// Copyright (C) characterRigCustom
// 
// File: sharingAttributeNode.cpp
//
// Dependency Graph Node: sharingAttribute
//
// Author: Maya Plug-in Wizard 2.0
//

#include "sharingAttribute.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MMessage.h>

#include <maya/MGlobal.h>

MTypeId     sharingAttribute::id( 0x83009 );

MObject     sharingAttribute::inputAttrs;
MObject     sharingAttribute::inputMessages;

sharingAttribute::sharingAttribute() {}
sharingAttribute::~sharingAttribute() {}

MStatus sharingAttribute::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;
	if( plug == inputMessages )
	{
		MArrayDataHandle inputAttrsHandle = data.inputArrayValue( inputAttrs, &returnStatus );

		if( returnStatus != MS::kSuccess )
			MGlobal::displayError( "Node sharingAttribute cannot get value\n" );
		else
		{
		}

	} else {
		return MS::kUnknownParameter;
	}

	return MS::kSuccess;
}

void* sharingAttribute::creator()
{
	return new sharingAttribute();
}

MStatus sharingAttribute::initialize()	
{
	MFnMessageAttribute msgAttr;
	MFnNumericAttribute nAttr;
	MStatus				stat;

	inputMessages = msgAttr.create( "inputMessages", "im" );
	msgAttr.setArray(true);

	stat = addAttribute( inputMessages );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	return MS::kSuccess;
}