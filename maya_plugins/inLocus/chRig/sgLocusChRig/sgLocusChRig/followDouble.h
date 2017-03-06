#ifndef _followDouble
#define _followDouble
//
// Copyright (C) MArrayTest
// 
// File: followDouble.h
//
// Dependency Graph Node: followDouble
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 

 
class followDouble : public MPxNode
{
public:
						followDouble();
	virtual				~followDouble(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     originalDouble;
	static  MObject		inputDouble;
	static  MObject     inputWeight;
	static  MObject		outputDouble;

	static	MTypeId		id;
};

#endif
