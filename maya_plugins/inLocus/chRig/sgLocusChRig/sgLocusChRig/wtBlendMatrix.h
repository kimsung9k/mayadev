#ifndef _wtBlendMatrixNode
#define _wtBlendMatrixNode
//
// Copyright (C) wtBlendMatrix
// 
// File: wtBlendMatrixNode.h
//
// Dependency Graph Node: wtBlendMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 


class wtBlendMatrix : public MPxNode
{
public:
						wtBlendMatrix();
	virtual				~wtBlendMatrix(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		inMatrix;
	static  MObject		outMatrix;

	static	MTypeId		id;
};

#endif
