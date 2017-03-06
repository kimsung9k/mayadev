#ifndef _squashNode
#define _squashNode
//
// Copyright (C) squash
// 
// File: squashNode.h
//
// Dependency Graph Node: squash
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

 
class squash : public MPxNode
{
public:
						squash();
	virtual				~squash(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		lengthOriginal;
	static  MObject		lengthModify;
	static  MObject     squashRate;
	static  MObject     forceValue;
	static  MObject     output;

	static	MTypeId		id;
};

#endif
