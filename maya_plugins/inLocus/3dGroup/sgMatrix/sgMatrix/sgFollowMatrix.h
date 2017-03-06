#ifndef _sgFollowMatrix
#define _sgFollowMatrix
//
// Copyright (C) MArrayTest
// 
// File: sgFollowMatrix.h
//
// Dependency Graph Node: sgFollowMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h> 

 
class sgFollowMatrix : public MPxNode
{
public:
						sgFollowMatrix();
	virtual				~sgFollowMatrix(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     originalMatrix;
	static  MObject		inputMatrix;
	static  MObject     inputWeight;
	static  MObject		outputMatrix;

	static	MTypeId		id;
};

#endif
