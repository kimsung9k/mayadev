#ifndef _blendTwoAngleNode
#define _blendTwoAngleNode
//
// Copyright (C) blendTwoAngle
// 
// File: blendTwoAngleNode.h
//
// Dependency Graph Node: blendTwoAngle
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTypeId.h> 

class blendTwoAngle : public MPxNode
{
public:
						blendTwoAngle();
	virtual				~blendTwoAngle(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		inAngle1;
	static  MObject		inAngle2;
	static  MObject     attributeBlender;
	static  MObject		outAngle;

	static	MTypeId		id;
};

#endif
