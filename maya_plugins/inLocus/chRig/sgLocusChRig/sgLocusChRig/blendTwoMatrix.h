#ifndef _blendTwoMatrixNode
#define _blendTwoMatrixNode
//
// Copyright (C) blendTwoMatrix
// 
// File: blendTwoMatrixNode.h
//
// Dependency Graph Node: blendTwoMatrix
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>


class blendTwoMatrix : public MPxNode
{
public:
						blendTwoMatrix();
	virtual				~blendTwoMatrix(); 

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