#ifndef _retargetTransNode_h
#define _retargetTransNode_h
//
// Copyright (C) Locus
// 
// File: retargetTransNode.h
//
// Dependency Graph Node: retargetTransNode
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MTypeId.h> 

 
class retargetTransNode : public MPxNode
{
public:
						retargetTransNode();
	virtual				~retargetTransNode(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static MStatus attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs );

public:
	static  MObject		aSourceMatrix;
	static  MObject     aSourceOrigMatrix;
	static  MObject     aSourceParentMatrix;

	static  MObject     aTargetOrigMatrix;
	static  MObject     aTargetParentMatrix;

	static  MObject     aDistanceRate;

	static  MObject     aLocalData;
		static  MObject     aLocalMatrix;

		static  MObject     aLocalMult;
			static  MObject     aLocalMultX;
			static  MObject     aLocalMultY;
			static  MObject     aLocalMultZ;

		static  MObject     aLocalOffset;

	static  MObject    aOriginalRate;

	static  MObject    aTransMatrix;

	static	MTypeId		id;
};

#endif
