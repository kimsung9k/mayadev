#ifndef _shoulderOrientNode
#define _shoulderOrientNode
//
// Copyright (C) shoulderOrient
// 
// File: shoulderOrientNode.h
//
// Dependency Graph Node: shoulderOrient
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MTypeId.h> 

 
class shoulderOrient : public MPxNode
{
public:
						shoulderOrient();
	virtual				~shoulderOrient(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	// There needs to be a MObject handle declared for each attribute that
	// the node will have.  These handles are needed for getting and setting
	// the values later.
	//
	static  MObject     aimAxis;
	static  MObject     upAxis;
	static  MObject		inputMatrix;
	static  MObject     outputMatrix;   // Example input attribute
	static  MObject		outAngleX;		// Example output attribute
	static  MObject		outAngleY;
	static  MObject		outAngleZ;


	// The typeid is a unique 32bit indentifier that describes this node.
	// It is used to save and retrieve nodes of this type from the binary
	// file format.  If it is not unique, it will cause file IO problems.
	//
	static	MTypeId		id;
};

#endif
