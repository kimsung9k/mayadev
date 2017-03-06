#ifndef _editMatrixByCurve_h
#define _editMatrixByCurve_h
//
// Copyright (C) Locus
// 
// File: editMatrixByCurve.h
//
// Dependency Graph Node: editMatrixByCurve
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h> 

 
class editMatrixByCurve : public MPxNode
{
public:
						editMatrixByCurve();
	virtual				~editMatrixByCurve(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static MStatus attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs );

public:
	static  MObject		aSourceMatrix;
	static  MObject     aUpMatrix;

	static  MObject     aSourceCurve;
	static  MObject     aDestCurve;

	static  MObject     aLockLength;

	static  MObject     aOutSourceMatrix;
	static  MObject     aOutDestMatrix;
	static  MObject     aOutOffsetMatrix;

	static	MTypeId		id;
};

#endif
