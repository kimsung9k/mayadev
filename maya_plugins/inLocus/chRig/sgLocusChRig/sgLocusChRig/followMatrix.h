#ifndef _followMatrix
#define _followMatrix
//
// Copyright (C) MArrayTest
// 
// File: followMatrix.h
//
// Dependency Graph Node: followMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h> 

 
class followMatrix : public MPxNode
{
public:
						followMatrix();
	virtual				~followMatrix(); 

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
