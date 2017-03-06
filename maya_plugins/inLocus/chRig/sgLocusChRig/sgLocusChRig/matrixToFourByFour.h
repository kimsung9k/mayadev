#ifndef _matrixToFourByFourNode
#define _matrixToFourByFourNode
//
// Copyright (C) matrixToFourByFour
// 
// File: matrixToFourByFourNode.h
//
// Dependency Graph Node: matrixToFourByFour
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 


class matrixToFourByFour : public MPxNode
{
public:
						matrixToFourByFour();
	virtual				~matrixToFourByFour(); 

	bool                allPlug( const MPlug& plug );
	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject		inMatrix;
	static  MObject     out[4][4];
	static	MTypeId		id;
};

#endif