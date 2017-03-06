#ifndef _dgTransform_h
#define _dgTransform_h
//
// Copyright (C) Locus
// 
// File: dgTransform.h
//
// Dependency Graph Node: dgTransform
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MTypeId.h> 

 
class dgTransform : public MPxNode
{
public:
						dgTransform();
	virtual				~dgTransform(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static MStatus attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs );

public:

	static  MObject		aTranslate;
		static  MObject		aTranslateX;
		static  MObject		aTranslateY;
		static  MObject		aTranslateZ;
	static  MObject		aRotate;
		static  MObject		aRotateX;
		static  MObject		aRotateY;
		static  MObject		aRotateZ;
	static  MObject		aScale;
		static  MObject		aScaleX;
		static  MObject		aScaleY;
		static  MObject		aScaleZ;
	static  MObject		aShear;
		static  MObject		aShearX;
		static  MObject		aShearY;
		static  MObject		aShearZ;
	static  MObject     aJointOrient;
		static  MObject     aJointOrientX;
		static  MObject     aJointOrientY;
		static  MObject     aJointOrientZ;


	static  MObject     aInputTranslate;
		static  MObject     aInputTranslateX;
		static  MObject     aInputTranslateY;
		static  MObject     aInputTranslateZ;
	static  MObject		aInputRotate;
		static  MObject		aInputRotateX;
		static  MObject		aInputRotateY;
		static  MObject		aInputRotateZ;
	static  MObject		aInputScale;
		static  MObject		aInputScaleX;
		static  MObject		aInputScaleY;
		static  MObject		aInputScaleZ;
	static  MObject		aInputShear;
		static  MObject		aInputShearX;
		static  MObject		aInputShearY;
		static  MObject		aInputShearZ;

	static  MObject		aMatrix;
	static  MObject     aInverseMatrix;
	static  MObject		aWorldMatrix;
	static  MObject		aWorldInverseMatrix;
	static  MObject		aParentMatrix;
	static  MObject		aParentInverseMatrix;

	static	MTypeId		id;

};

#endif
