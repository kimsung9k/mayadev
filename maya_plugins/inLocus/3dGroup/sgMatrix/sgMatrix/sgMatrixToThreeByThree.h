#ifndef _matrixToThreeByThreeNode
#define _matrixToThreeByThreeNode
//
// Copyright (C) matrixToThreeByThree
// 
// File: matrixToThreeByThreeNode.h
//
// Dependency Graph Node: matrixToThreeByThree
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 


class sgMatrixToThreeByThree : public MPxNode
{
public:
						sgMatrixToThreeByThree();
	virtual				~sgMatrixToThreeByThree(); 

	bool                allPlug( const MPlug& plug );
	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		inMatrix;
	static  MObject     out00;
	static  MObject     out01;
	static  MObject     out02;
	static  MObject     out10;
	static  MObject     out11;
	static  MObject     out12;
	static  MObject     out20;
	static  MObject     out21;
	static  MObject     out22;
	static	MTypeId		id;
};

#endif