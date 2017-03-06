#ifndef _sgBlendTwoMatrixNode
#define _sgBlendTwoMatrixNode
//
// Copyright (C) sgBlendTwoMatrix
// 
// File: sgBlendTwoMatrixNode.h
//
// Dependency Graph Node: sgBlendTwoMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>


class sgBlendTwoMatrix : public MPxNode
{
public:
						sgBlendTwoMatrix();
	virtual				~sgBlendTwoMatrix(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static  MObject		inMatrix1;
	static  MObject		inMatrix2;
	static  MObject     attributeBlender;
	static  MObject		outMatrix;
	static  MObject     outInvMatrix;

	static	MTypeId		id;
};

#endif