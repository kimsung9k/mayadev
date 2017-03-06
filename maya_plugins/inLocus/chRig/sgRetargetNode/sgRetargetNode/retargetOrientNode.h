#ifndef _retargetOrientNode_h
#define _retargetOrientNode_h
//
// Copyright (C) Locus
// 
// File: retargetOrientNode.h
//
// Dependency Graph Node: retargetOrientNode
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MTypeId.h> 

 
class retargetOrientNode : public MPxNode
{
public:
						retargetOrientNode();
	virtual				~retargetOrientNode(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:
	static MStatus      attributeAffectsArray( MObject& affectAttr, MObject** affectedAttrs );

public:

	static  MObject		aSourceMatrix;
	static  MObject     aSourceOrigMatrix;
	static  MObject     aSourceParentMatrix;

	static  MObject     aTargetOrigMatrix;
	static  MObject     aTargetParentMatrix;

	static  MObject     aLocalData;
		static  MObject     aLocalMatrix;
		static  MObject     aLocalInOffset;
		static  MObject     aLocalOutOffset;
		static  MObject     aLocalMult;

	static  MObject    aOrient;
		static  MObject    aOrientX;
		static  MObject    aOrientY;
		static  MObject    aOrientZ;

	static  MObject    aOriginalRate;
		
	static  MObject    aOrientMatrix;

	static	MTypeId		id;

};

#endif
